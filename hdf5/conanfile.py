from conans import ConanFile, CMake
from conans.tools import download, unzip

class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.10.5"
    license = "BSD-style Open Source"
    url = "https://support.hdfgroup.org/ftp/HDF5/releases"
    author = "The HDF Group"
    description = "High-performance data management and storage library"
    settings = "os", "compiler", "build_type", "arch"
    generators = "cmake"

    def source(self):
        # https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.10/hdf5-1.10.5/src/CMake-hdf5-1.10.5.zip
        # https://support.hdfgroup.org/ftp/HDF5/releases
        pkg_name = "CMake-hdf5-1.10.5.zip"
        download(self.url + "/hdf5-1.10/hdf5-1.10.5/src/" + pkg_name, pkg_name)
        unzip(pkg_name)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="CMake-hdf5-1.10.5/hdf5-1.10.5")
        cmake.build()
        cmake.install()
