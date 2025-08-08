# Example programs
set(EXAMPLE_SOURCES
    basic_usage.cpp
    bloom_filter_demo.cpp
    error_propagation.cpp
    function_equality.cpp
    miller_rabin.cpp
    hash_set_example.cpp
    hash_map_example.cpp
)

# Create executable for each example
foreach(example_source ${EXAMPLE_SOURCES})
    get_filename_component(example_name ${example_source} NAME_WE)
    add_executable(${example_name} ${example_source})
    
    target_link_libraries(${example_name}
        PRIVATE
            Bernoulli::Types
    )
    
    set_target_properties(${example_name} PROPERTIES
        CXX_STANDARD 20
        CXX_STANDARD_REQUIRED ON
        RUNTIME_OUTPUT_DIRECTORY "${CMAKE_BINARY_DIR}/bin/examples"
    )
endforeach()

# Add custom target to build all examples
add_custom_target(examples
    DEPENDS ${EXAMPLE_SOURCES}
    COMMENT "Building all examples"
)
