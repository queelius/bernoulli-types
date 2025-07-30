# Find or fetch Google Test
include(FetchContent)
FetchContent_Declare(
    googletest
    GIT_REPOSITORY https://github.com/google/googletest.git
    GIT_TAG        v1.14.0
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

# Enable testing
enable_testing()

# Collect all test source files
set(TEST_SOURCES
    test_rate_span.cpp
    test_observed_bool.cpp
    test_observed_set.cpp
    test_observed_map.cpp
    test_bloom_filter.cpp
    test_error_propagation.cpp
    test_hash_set.cpp
)

# Create test executable
add_executable(bernoulli_tests ${TEST_SOURCES})

# Link against Google Test and our library
target_link_libraries(bernoulli_tests
    PRIVATE
        Bernoulli::Types
        GTest::gtest_main
        GTest::gtest
)

# Add include directories for tests
target_include_directories(bernoulli_tests
    PRIVATE
        ${CMAKE_CURRENT_SOURCE_DIR}
)

# Set test properties
set_target_properties(bernoulli_tests PROPERTIES
    CXX_STANDARD 17
    CXX_STANDARD_REQUIRED ON
)

# Register tests with CTest
include(GoogleTest)
gtest_discover_tests(bernoulli_tests)

# Add custom target to run tests with output
add_custom_target(check
    COMMAND ${CMAKE_CTEST_COMMAND} --output-on-failure
    DEPENDS bernoulli_tests
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
    COMMENT "Running unit tests"
)

# Add valgrind target if available
find_program(VALGRIND_COMMAND valgrind)
if(VALGRIND_COMMAND)
    add_custom_target(valgrind
        COMMAND ${VALGRIND_COMMAND} --leak-check=full --error-exitcode=1 $<TARGET_FILE:bernoulli_tests>
        DEPENDS bernoulli_tests
        WORKING_DIRECTORY ${CMAKE_BINARY_DIR}
        COMMENT "Running tests under valgrind"
    )
endif()