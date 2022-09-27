cmake_minimum_required(VERSION 3.10)
project(benchmark VERSION 1.0)

find_library(GMP gmp)

add_executable(benchmark benchmark.c)

target_compile_options(benchmark PRIVATE -Ofast -march=native)

include(CheckCXXCompilerFlag)
check_cxx_compiler_flag("-mavx2" COMPILER_SUPPORTS_AVX2)
if(COMPILER_SUPPORTS_AVX2)
    target_compile_options(benchmark PRIVATE -mavx2)
endif()

target_link_libraries(benchmark ${GMPXX} ${GMP})