# ========================= LICENSE =================================
#
# Copyright (C) 2022 Continental Corporation
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#      http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
# ========================= LICENSE =================================

cmake_minimum_required(VERSION 3.4)
project(ecal-camera-samples)

set(CPACK_PACKAGE_NAME ${PROJECT_NAME})
set(CPACK_PACKAGE_DESCRIPTION_SUMMARY ${PROJECT_NAME})

set(CPACK_PACKAGE_VERSION_MAJOR 1)
set(CPACK_PACKAGE_VERSION_MINOR 0)
set(CPACK_PACKAGE_VERSION_PATCH 0)
set(CPACK_PACKAGE_INSTALL_DIRECTORY ${PROJECT_NAME})
set(CPACK_PACKAGE_CONTACT "mirza.canovic@gmail.com")
set(CPACK_OUTPUT_FILE_PREFIX _deploy)

set(CPACK_DEBIAN_PACKAGE_SHLIBDEPS ON)

include(CPack)

add_definitions(-DQWT_DLL)
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)
if(UNIX)
 set(CMAKE_LINK_WHAT_YOU_USE ON)
endif(UNIX)
# Set CMake policy behavior (alias targets)
cmake_policy(SET CMP0028 NEW)
cmake_policy(SET CMP0048 NEW)
cmake_policy(SET CMP0057 NEW)
cmake_policy(SET CMP0054 NEW)
cmake_policy(SET CMP0080 NEW)

# --------------------------------------------------------
# set ECAL_MON_PLUGIN_DIR install dir
# --------------------------------------------------------
include(GNUInstallDirs)
if(WIN32)
  set(ECAL_MON_PLUGIN_DIR ecalmon_plugins)
else()
  set(ECAL_MON_PLUGIN_DIR ecal/plugins/mon)
endif()

set(eCAL_install_lib_dir  ${CMAKE_INSTALL_LIBDIR})
set(eCAL_install_bin_dir  ${CMAKE_INSTALL_BINDIR})


include(${CMAKE_CURRENT_SOURCE_DIR}/cmake_utils/mon_functions.cmake)

# --------------------------------------------------------
# command line build options
# use it that way cmake .. -DHAS_OPENCV=ON
# --------------------------------------------------------
include(CMakeDependentOption)

if(WIN32)
    include(${CMAKE_CURRENT_LIST_DIR}/cmake_utils/qt/qt_windeployqt.cmake)
endif()

set(THREADS_PREFER_PTHREAD_FLAG ON)

add_subdirectory(ecal_camera_snd)
add_subdirectory(camera_receiver_mon_plugin)
