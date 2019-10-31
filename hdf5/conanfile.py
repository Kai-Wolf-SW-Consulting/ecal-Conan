from conans import ConanFile, CMake
from conans.tools import download, get, patch, unzip


class Hdf5Conan(ConanFile):
    name = "hdf5"
    version = "1.8.21"
    license = "BSD-style Open Source"
    url = "https://support.hdfgroup.org/ftp/HDF5/releases"
    author = "The HDF Group"
    topics = ("c++", "I/O", "File format")
    description = "High-performance data management and storage library"
    settings = "os", "compiler", "arch"
    exports_sources = "cmake_config_folder.patch"
    generators = "cmake"

    def source(self):
        pkg_name = "CMake-hdf5-1.8.21.zip"
        download(self.url + "/hdf5-1.8/hdf5-1.8.21/src/" + pkg_name, pkg_name)
        unzip(pkg_name)
        patch(base_path="CMake-hdf5-1.8.21/hdf5-1.8.21",
              patch_file="cmake_config_folder.patch",
              strip=1)

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="CMake-hdf5-1.8.21/hdf5-1.8.21")
        cmake.build()
        cmake.install()
