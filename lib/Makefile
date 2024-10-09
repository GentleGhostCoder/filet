# Set the default target to all so that when you invoke make without arguments, it will execute the all target.
.PHONY: all clean

all: build_project install_project

# Target for creating the build directory and running the CMake configuration step
build_project:
	cd catch2 &&  \
	cmake -Bbuild -H. -DBUILD_TESTING=OFF && \
	cmake --build build/

# Target for installing the project to the desired directory
# Target for installing the project to the desired directory
install_project:
	# check if lib/catch2/target/include exists (if not run install)
	if [ ! -d "catch2/target/include" ]; then \
		cd catch2 &&  \
		cmake --install ./build --prefix target; \
	fi

# Target for cleaning up the build and target directories
clean:
	rm -rf lib/catch2/build lib/catch2/target
