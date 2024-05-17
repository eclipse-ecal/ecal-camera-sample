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

cmake_minimum_required(VERSION 3.14)

# Allow the install command to use generator expressions
if(POLICY CMP0087)
    cmake_policy(SET CMP0087 NEW)
endif()

set(CMAKE_FIND_PACKAGE_PREFER_CONFIG ON)

project(ecal_camera_snd)

# Legacy Qt5 (pre 5.15) support as suggested by teh Qt Documentation:
# https://doc.qt.io/qt-6/cmake-qt5-and-qt6-compatibility.html#supporting-older-qt-5-versions
find_package(QT NAMES Qt6 Qt5 REQUIRED COMPONENTS Core Widgets MultimediaWidgets)
find_package(Qt${QT_VERSION_MAJOR} REQUIRED COMPONENTS Core Widgets MultimediaWidgets)

find_package(eCAL REQUIRED)
find_package(Protobuf REQUIRED)

set(CMAKE_AUTOMOC ON)

set(source_files
  main.cpp
  camera_wrapper.h
  camera_wrapper.cpp
  camera_wrapper_with_fps_control.h
  camera_wrapper_with_fps_control.cpp
)

set(protobuf_files
    ${CMAKE_SOURCE_DIR}/proto_messages/compressed_image.proto
)

add_executable(${PROJECT_NAME} ${source_files})

PROTOBUF_TARGET_CPP(${PROJECT_NAME} ${CMAKE_SOURCE_DIR}/proto_messages/ ${protobuf_files})

target_link_libraries(${PROJECT_NAME}
  eCAL::core
  protobuf::libprotobuf
  Qt${QT_VERSION_MAJOR}::Core
  Qt${QT_VERSION_MAJOR}::Widgets
  Qt${QT_VERSION_MAJOR}::MultimediaWidgets
  Qt${QT_VERSION_MAJOR}::Multimedia
)

target_compile_features(${PROJECT_NAME} PRIVATE cxx_std_14) 

if ((WIN32 OR APPLE) AND (${QT_VERSION_MAJOR} GREATER_EQUAL 6))

    # Generate a script that will deploy all necessary Qt DLLs to the binary folder
    # https://doc.qt.io/qt-6/qt-deploy-runtime-dependencies.html
    # Available for Qt 6.3 and up (=> Not for Qt5!)
    # Executing it requires CMake 3.14 and up, due to policy https://cmake.org/cmake/help/latest/policy/CMP0087.html
    qt_generate_deploy_app_script(
        TARGET ${PROJECT_NAME}
        OUTPUT_SCRIPT qt_deploy_script
        NO_COMPILER_RUNTIME
        NO_UNSUPPORTED_PLATFORM_ERROR
    )

    # Add a postbuild script that will also execute the created script via cmake -P
    # This is necessary to make the application startable / debuggable from the build directory.
    add_custom_command(TARGET ${PROJECT_NAME} POST_BUILD
        COMMAND ${CMAKE_COMMAND} -DQT_DEPLOY_PREFIX=$<TARGET_FILE_DIR:${PROJECT_NAME}> -DQT_DEPLOY_BIN_DIR=. -P ${qt_deploy_script}
    )

    # Use the script for deploying the qt dlls in the install dir
    install(SCRIPT ${qt_deploy_script})

elseif(WIN32)

    # For Qt5 we use our legacy script.
    # Deploy Qt DLLs in the binary folder. This is necessary for starting the application from whithin the IDE without having to copy QtCore.dll, QtWidgets.dll etc. by hand each time
    qt_add_windeployqt_postbuild(--no-system-d3d-compiler --no-compiler-runtime --no-opengl-sw --pdb "$<TARGET_FILE:${PROJECT_NAME}>")

    get_target_property(_qmake_executable Qt5::qmake IMPORTED_LOCATION)
    get_filename_component(_qt_bin_dir "${_qmake_executable}" DIRECTORY)
    find_program(WINDEPLOYQT_EXECUTABLE windeployqt HINTS "${_qt_bin_dir}")
    install(CODE
        "
        set(_file ${CMAKE_RUNTIME_OUTPUT_DIRECTORY}/Release/ecal_mon_gui.exe)
        execute_process(
                COMMAND \"${CMAKE_COMMAND}\" -E
                    env PATH=\"${_qt_bin_dir}\" \"${WINDEPLOYQT_EXECUTABLE}\"
                        --dry-run
                        --no-compiler-runtime
                        --no-angle
                        --no-opengl-sw
                        --list mapping
                        \${_file}
                OUTPUT_VARIABLE _output
                OUTPUT_STRIP_TRAILING_WHITESPACE
            )
        separate_arguments(_files WINDOWS_COMMAND \${_output})
        while(_files)
                list(GET _files 0 _src)
                list(GET _files 1 _dest)
                execute_process(
                    COMMAND \"${CMAKE_COMMAND}\" -E
                        copy \${_src} \"\${CMAKE_INSTALL_PREFIX}/bin/\${_dest}\"
                )
                list(REMOVE_AT _files 0 1)
        endwhile()
        "
)
endif()