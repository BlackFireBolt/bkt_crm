$(document).ready(function() {
var dt_table = $('.datatable').dataTable({
        language: dt_language,  // global variable defined in html
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        order: [[ 0, "desc" ]],
        searching: true,
        columnDefs: [
            {
                data: 'id',
                targets: [0],
                orderable: true,
            },
            {
                data: 'status',
                targets: [1],
                orderable: true,
            },
            {
                data: 'name',
                targets: [2],
                orderable: true,
            },
            {
                data: 'phone',
                targets: [3],
                orderable: true,
            },
            {
                data: 'country',
                targets: [4],
                orderable: true,
            },
            {
                data: 'created_date',
                targets: [5],
                orderable: true,
            },
        ],
        processing: true,
        serverSide: true,
        stateSave: true,
        ajax: MARKET_LIST_JSON_URL
    });
    });