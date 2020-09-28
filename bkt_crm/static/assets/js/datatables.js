$(document).ready(function() {
    var dt_table = $('.datatable').dataTable({
        language: dt_language,  // global variable defined in html
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        order: [[ 0, "desc" ]],
        searching: false,
        columnDefs: [
            {
             className: "center",
             targets: [0, 1, 2, 3, 4, 5, 6, 7]
            },
            {
                data: 'id',
                targets: [0]
            },
            {
                data: 'status',
                targets: [1]
            },
            {
                data: 'name',
                targets: [2]
            },
            {
                data: 'phone',
                targets: [3]
            },
            {
                data: 'country',
                targets: [4]
            },
            {
                data: 'email',
                targets: [5]
            },
            {
                data: 'created_date',
                targets: [6]
            },
            {
                data: 'manager',
                targets: [7]
            },
        ],

        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: ADMIN_LIST_JSON_URL
    });
});