cmake_minimum_required(VERSION 3.15)
project(test_webrtc_apm CXX)

find_package(webrtc-apm REQUIRED CONFIG)

add_executable(test_webrtc_apm test_package.cpp)
target_link_libraries(test_webrtc_apm webrtc-apm::webrtc-apm)
target_compile_features(test_webrtc_apm PRIVATE cxx_std_17)
