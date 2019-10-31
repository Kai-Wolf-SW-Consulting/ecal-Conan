from conans import ConanFile, tools


class AsioConan(ConanFile):
    name = "asio"
    version = "1.14.0"
    license = "Boost Software License"
    author = "Chris Kohlhoff"
    url = "https://github.com/chriskohlhoff/asio"
    description = "Asio C++ Library"
    topics = ("c++", "asio")
    no_copy_sources = True

    def source(self):
        pkg_name = "%s-%s" % (self.name, self.version.replace(".", "-"))
        zip_name = self.name + "-" + pkg_name + ".zip"
        tools.download("%s/archive/%s.zip" % (self.url, pkg_name), zip_name)
        tools.unzip(zip_name)

    def package(self):
        src_folder = "%s-%s-%s" % (self.name, self.name, self.version.replace(".", "-"))
        self.copy("*.hpp", "include", "%s/asio/include" % src_folder)
        self.copy("*.ipp", "include", "%s/asio/include" % src_folder)

    def package_info(self):
        self.cpp_info.defines.append('ASIO_STANDALONE')

    def package_id(self):
        self.info.header_only()
