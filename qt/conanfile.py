from conans import ConanFile, tools
from distutils.spawn import find_executable
from os import environ, path
from shutil import move


class QtConan(ConanFile):
    name = "Qt"
    version = "5.12.4"
    description = "Qt cross-platform framework for GUIs"
    url = "http://download.qt.io/official_releases/qt"
    author = "Qt"
    license = "LGPL-3.0"
    topics = ("qt", "gui", "framework")
    exports_sources = ["CMakeLists.txt"]
    generators = "cmake"
    settings = "os", "arch", "compiler", "build_type"
    submodules = [
        "qt3d", "qtactiveqt", "qtandroidextras", "qtcanvas3d", "qtcharts", "qtconnectivity",
        "qtdatavis3d", "qtdeclarative", "qtdoc", "qtgamepad", "qtgraphicaleffects",
        "qtimageformats", "qtlocation", "qtmacextras", "qtmultimedia", "qtnetworkauth",
        "qtpurchasing", "qtquickcontrols", "qtquickcontrols2", "qtremoteobjects", "qtscript",
        "qtscxml", "qtsensors", "qtserialbus", "qtserialport", "qtspeech", "qtsvg", "qttools",
        "qttranslations", "qtvirtualkeyboard", "qtwayland", "qtwebchannel", "qtwebengine",
        "qtwebsockets", "qtwebview", "qtwinextras", "qtx11extras", "qtxmlpatterns"
    ]
    options = dict(
        {
            "shared": [True, False],
            "fPIC": [True, False],
            "opengl": ["no", "es2", "desktop", "dynamic"],
            "openssl": ["no", "yes", "linked"],
        }, **{module[2:]: [True, False] for module in submodules})
    no_copy_source = True
    default_options = ("shared=True", "fPIC=True", "opengl=desktop", "openssl=no") + tuple(
        module[2:] + "=True" if module in ["qtxmlpatterns", "qtwinextras"] else module[2:] + "=False"
        for module in submodules)
    short_paths = True
    build_policy = "missing"

    def build_requirements(self):
        if tools.os_info.is_linux:
            pack_names = [
                "libfontconfig1-dev", "libfreetype6-dev", "libgl1-mesa-dev", "libx11-dev",
                "libx11-xcb-dev", "libxcb-glx0-dev", "libxcb-icccm4-dev", "libxcb-image0-dev",
                "libxcb-keysyms1-dev", "libxcb-randr0-dev", "libxcb-render-util0-dev",
                "libxcb-shape0-dev", "libxcb-shm0-dev", "libxcb-sync-dev", "libxcb-xfixes0-dev",
                "libxcb1-dev", "libxext-dev", "libxfixes-dev", "libxi-dev", "libxkbcommon-x11-dev",
                "libxrender-dev"
            ]

            if self.settings.arch == "x86":
                pack_names = [item + ":i386" for item in pack_names]

            installer = tools.SystemPackageTool()
            installer.update()
            installer.install(" ".join(pack_names))

    def requirements(self):
        if self.options.openssl == "yes":
            self.requires("OpenSSL/1.1.0g@conan/stable")
            self.options["OpenSSL"].no_zlib = True
            self.options["OpenSSL"].shared = True
        if self.options.openssl == "linked":
            self.requires("OpenSSL/1.1.0g@conan/stable")
            self.options["OpenSSL"].no_zlib = True
            self.options["OpenSSL"].shared = False

        if tools.os_info.is_linux:
            pack_names = [
                "libfontconfig1", "libxrender1", "libxext6", "libxfixes3", "libxi6",
                "libgl1-mesa-dri", "libxcb1", "libx11-xcb1", "libxcb-keysyms1", "libxcb-image0",
                "libxcb-shm0", "libx11-6", "libxcb-icccm4", "libxcb-sync1", "libxcb-xfixes0",
                "libxcb-shape0", "libxcb-render-util0", "libxcb-randr0", "libxcb-glx0"
            ]

            if self.settings.arch == "x86":
                pack_names = [item + ":i386" for item in pack_names]

            installer = tools.SystemPackageTool()
            installer.update()
            installer.install(" ".join(pack_names))

    def source(self):
        url = self.url + "/{0}/{1}/single/qt-everywhere-src-{1}"\
            .format(self.version[:self.version.rfind('.')], self.version)
        if tools.os_info.is_windows:
            tools.get("%s.zip" % url)
        else:
            self.run("wget -qO- %s.tar.xz | tar -xJ " % url)
        move("qt-everywhere-src-%s" % self.version, "qt5")

    def build(self):
        args = [
            "-opensource", "-confirm-license", "-nomake examples", "-nomake tests",
            "-prefix %s" % self.package_folder
        ]
        if not self.options.shared:
            args.insert(0, "-static")
            if self.settings.os == "Windows":
                if self.settings.compiler.runtime == "MT" or self.settings.compiler.runtime == "MTd":
                    args.append("-static-runtime")
        else:
            args.insert(0, "-shared")
        if self.settings.build_type == "Debug":
            args.append("-debug")
        else:
            args.append("-release")

        for module in self.submodules:
            if not getattr(self.options, module[2:]):
                args.append("-skip " + module)

        # OpenGL
        if self.options.opengl == "no":
            args += ["-no-opengl"]
        elif self.options.opengl == "es2":
            args += ["-opengl es2"]
        elif self.options.opengl == "desktop":
            args += ["-opengl desktop"]
        if self.settings.os == "Windows":
            if self.options.opengl == "dynamic":
                args += ["-opengl dynamic"]

        # OpenSSL
        if self.options.openssl == "no":
            args += ["-no-openssl"]
        elif self.options.openssl == "yes":
            args += ["-openssl"]
        else:
            args += ["-openssl-linked"]
        if self.options.openssl != "no":
            args += ["-I%s" % i for i in self.deps_cpp_info["OpenSSL"].include_paths]
            libs = self.deps_cpp_info["OpenSSL"].libs
            lib_paths = self.deps_cpp_info["OpenSSL"].lib_paths
            args += [
                "OPENSSL_LIBS=\"%s %s\"" %
                (" ".join(["-L" + i for i in lib_paths]), " ".join(["-l" + i for i in libs]))
            ]
        if self.settings.os == "Windows":
            if self.settings.compiler == "Visual Studio":
                self._build_msvc(args)
            else:
                self._build_mingw(args)
        else:
            self._build_unix(args)

    def _build_msvc(self, args):
        build_command = find_executable("jom.exe")
        if build_command:
            build_args = ["-j", str(tools.cpu_count())]
        else:
            build_command = "nmake.exe"
            build_args = []
        self.output.info("Using '%s %s' to build" % (build_command, " ".join(build_args)))

        vcvars = tools.vcvars_command(self.settings)

        self.run("%s && set" % vcvars)
        self.run("%s && %s/qt5/configure %s" % (vcvars, self.source_folder, " ".join(args)))
        self.run("%s && %s %s" % (vcvars, build_command, " ".join(build_args)))
        self.run("%s && %s install" % (vcvars, build_command))

    def _build_mingw(self, args):
        # Workaround for configure using clang first if in the path
        new_path = []
        for item in environ['PATH'].split(';'):
            if item != 'C:\\Program Files\\LLVM\\bin':
                new_path.append(item)
        environ['PATH'] = ';'.join(new_path)

        args += ["-platform win32-g++"]

        with tools.environment_append({"MAKEFLAGS": "-j %d" % tools.cpu_count()}):
            self.output.info("Using '%d' threads" % tools.cpu_count())
            self.run("%s/qt5/configure.bat %s" % (self.source_folder, " ".join(args)))
            self.run("mingw32-make")
            self.run("mingw32-make install")

    def _build_unix(self, args):
        if self.settings.os == "Linux":
            args += ["-silent", "-qt-xcb"]
            if self.settings.arch == "x86":
                args += ["-platform linux-g++-32"]
        else:
            args += ["-silent", "-no-framework"]
            if self.settings.arch == "x86":
                args += ["-platform macx-clang-32"]

        with tools.environment_append({"MAKEFLAGS": "-j %d" % tools.cpu_count()}):
            self.output.info("Using '%d' threads" % tools.cpu_count())
            self.run("%s/qt5/configure %s" % (self.source_folder, " ".join(args)))
            self.run("make")
            self.run("make install")

    def package_info(self):
        if self.settings.os == "Windows":
            self.env_info.path.append(path.join(self.package_folder, "bin"))
        self.env_info.CMAKE_PREFIX_PATH.append(self.package_folder)
