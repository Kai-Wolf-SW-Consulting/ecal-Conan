from conans import ConanFile, tools


class SimpleiniConan(ConanFile):
    name = "simpleini"
    version = "4.17"
    license = "MIT License"
    author = "Brodie Thiesfield"
    url = "https://github.com/brofield/simpleini"
    description = "Simple library to read and write INI-style configuration files"
    topics = ("c++", "INI files", "configuration files")
    no_copy_sources = True
    exports_sources = ["include/*"]

    def source(self):
        pkg_name = "%s-%s.zip" % (self.name, self.version)
        tools.download("%s/archive/%s.zip" % (self.url, self.version), pkg_name)
        tools.unzip(pkg_name)

    def package(self):
        self.copy("*.h", "include", "%s-%s" % (self.name, self.version))
