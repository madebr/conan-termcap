from conans import ConanFile, AutoToolsBuildEnvironment, tools
import os

class TermcapConan(ConanFile):
    name = "termcap"
    version = "1.3.1"
    description = "Termcap is a library and data base that enables programs to use display terminals in a terminal-independent manner."
    topics = ["conan", "termcap", "terminal"]
    url = "https://github.com/bincrafters/conan-termcap"
    homepage = "https://www.gnu.org/software/termutils/manual/termcap-1.3/termcap.html"
    author = "Bincrafters <bincrafters@gmail.com>"
    license = "GPLv2"
    settings = "os", "compiler", "build_type", "arch"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
    }
    _source_subfolder = "sources"

    def configure(self):
        if self.settings.compiler != "Visual Studio":
            del self.settings.compiler.libcxx

    def source(self):
        url = "https://ftp.gnu.org/gnu/termcap/{}-{}.tar.gz".format(self.name, self.version)
        tools.get(url, sha256="91a0e22e5387ca4467b5bcb18edf1c51b930262fd466d5fda396dd9d26719100")
        extracted_dir = "{}-{}".format(self.name, self.version)
        os.rename(extracted_dir, self._source_subfolder)

        tools.replace_in_file(os.path.join(self.source_folder, self._source_subfolder, "Makefile.in"),
                              "CFLAGS = -g",
                              "")

    def build(self):
        autoTools = AutoToolsBuildEnvironment(self)
        autoTools.configure(configure_dir=os.path.join(self.source_folder, self._source_subfolder))
        autoTools.make()

    def package(self):
        with tools.chdir(self.build_folder):
            autoTools = AutoToolsBuildEnvironment(self)
            autoTools.install()
        self.copy("COPYING", src=os.path.join(self.source_folder, self._source_subfolder), dst="licenses")

    def package_info(self):
        self.cpp_info.includedirs = ["include"]
        self.cpp_info.libdirs = ["lib"]
        self.cpp_info.libs = ["termcap"]
