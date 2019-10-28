from conans import ConanFile, CMake, tools
from conans.tools import download, unzip, replace_in_file
from os import getcwd, path

class SpdlogConan(ConanFile):
    name = "spdlog"
    version = "0.16.3"
    license = "MIT License"
    author = "Gabi Melman <gmelman1@gmail.com>"
    url = "https://github.com/gabime/spdlog"
    description = "Very fast, header only, C++ logging library"
    topics = ("c++", "logging")
    no_copy_source = True

    def source(self):
        # https://github.com/gabime/spdlog/archive/v0.16.3.zip
        pkg_name = "v" + self.version + ".zip"
        download(self.url + "/archive/" + pkg_name, pkg_name)
        unzip(pkg_name)

    def build(self):
        cmake = CMake(self)
        defs = {"SPDLOG_BUILD_EXAMPLES": "OFF", "SPDLOG_BUILD_TESTING": "OFF"}
        source_folder = self.name + "-" + self.version
        cmake.configure(defs=defs, source_folder=source_folder)
        self.build_folder = getcwd()
        cmake.build()

        # Fix broken package version and 32/64 bit issues
        build_spdlog_conf = path.join(self.build_folder,
                                      "spdlogConfigVersion.cmake")
        replace_in_file(
            build_spdlog_conf,
            "# if the installed or the using project don't have " \
            "CMAKE_SIZEOF_VOID_P set, ignore it:",
            "return()",
            strict=False)
        replace_in_file(
            build_spdlog_conf, "0.16.2", "0.16.3", strict=False)
        cmake.install()


