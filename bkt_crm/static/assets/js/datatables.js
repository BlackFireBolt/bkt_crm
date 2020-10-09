$(document).ready(function() {
    var dt_table = $('.datatable').DataTable({
        language: dt_language,  // global variable defined in html
        lengthMenu: [[25, 50, 100, 200], [25, 50, 100, 200]],
        order: [[ 1, "desc" ]],
        searching: false,
        columnDefs: [
            {
                data: null,
                defaultContent: '',
                orderable: false,
                className: 'select-checkbox',
                targets: [0]
            },
            {
                data: 'id',
                targets: [1],
                orderable: true,
            },
            {
                data: 'status',
                targets: [2],
                orderable: true,
            },
            {
                data: 'name',
                targets: [3],
                orderable: true,
            },
            {
                data: 'phone',
                targets: [4],
                orderable: true,
            },
            {
                data: 'country',
                targets: [5],
                orderable: true,
            },
            {
                data: 'email',
                targets: [6],
                orderable: true,
            },
            {
                data: 'depozit',
                targets: [7],
                orderable: true,
            },
            {
                data: 'created_date',
                targets: [8],
                orderable: true,
            },
            {
                data: 'manager',
                targets: [9],
                orderable: true,
            },
        ],
        select: {
            style:    'multi',
            selector: 'td:first-child'
        },
        processing: true,
        full_row_select: true,
        serverSide: true,
        stateSave: true,
        createdRow: function( row, data, dataIndex ) {
                             switch($(data['status']).text()){
                                    case 'Новый':
                                            $("td:eq(0)",row).addClass('table_new');
                                            break;
                                    case 'Аут':
                                            $("td:eq(0)",row).addClass('table_aut');
                                            break;
                                    case 'Не интересно':
                                            $("td:eq(0)",row).addClass('table_notinteres');
                                            break;
                                    case 'Потенциал':
                                            $("td:eq(0)",row).addClass('table_potential');
                                            break;
                                    case 'Не отвечает':
                                            $("td:eq(0)",row).addClass('table_na');
                                            break;
                                    case 'Клиент':
                                            $("td:eq(0)",row).addClass('table_client');
                                            break;
                                    case 'Горячий':
                                            $("td:eq(0)",row).addClass('table_hot');
                                            break;
                            }
        },
        ajax: ADMIN_LIST_JSON_URL
    });
    dt_table.on("click", "th.select-checkbox", function() {
    if ($("th.select-checkbox").hasClass("selected")) {
        dt_table.rows().deselect();
        $("th.select-checkbox").removeClass("selected");
    } else {
        dt_table.rows().select();
        $("th.select-checkbox").addClass("selected");
    }
    }).on("select deselect", function() {
    ("Some selection or deselection going on")
    if (dt_table.rows({
            selected: true
        }).count() !== dt_table.rows().count()) {
        $("th.select-checkbox").removeClass("selected");
    } else {
        $("th.select-checkbox").addClass("selected");
    }
    });
});