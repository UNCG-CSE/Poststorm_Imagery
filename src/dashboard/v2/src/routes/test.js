const test_json = {
    "py/object": "psic.assigner.batch.Batch",
    path: "F:Shared drivesP-SickdataFlorence",
    small_path: "F:Shared drivesP-SicksmallFlorence",
    user_id: "Derp",
    debug: true,
    operations: [
        {
            command: "tag",
            tag_operation: "add",
            tag: "some_bool_tag",
            content: true
        },
        {
            command: "tag",
            tag_operation: "add",
            tag: "some_int_tag",
            content: 1
        },
        {
            command: "tag",
            tag_operation: "add_notes",
            content: "Hello world, how are you?"
        },
        {
            command: "tag",
            tag_operation: "next"
        }
    ]
}

console.log(test_json["py/object"])