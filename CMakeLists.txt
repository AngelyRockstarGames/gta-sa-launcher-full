cmake_minimum_required(VERSION 3.10)
project(version_guard)
add_library(version SHARED version.cpp version.def)
