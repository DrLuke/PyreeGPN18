cmake_minimum_required(VERSION 3.5)
project(vdpau)

set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -std=c99")

set(SOURCE_FILES viddecode.c)
add_executable(dummy ${SOURCE_FILES})

TARGET_LINK_LIBRARIES(dummy ffmpeg)