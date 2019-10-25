from conans import ConanFile, CMake
from conans.tools import download, unzip

class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.8.21"
    license = "BSD-style Open Source"
    url = "https://support.hdfgroup.org/ftp/HDF5/releases"
    author = "The HDF Group"
    description = "High-performance data management and storage library"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        pkg_name = "CMake-hdf5-1.8.21.zip"
        download(self.url + "/hdf5-1.8/hdf5-1.8.21/src/" + pkg_name, pkg_name)
        unzip(pkg_name)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="CMake-hdf5-1.8.21/hdf5-1.8.21")
        cmake.build()
        cmake.install()
