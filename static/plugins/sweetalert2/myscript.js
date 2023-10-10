
// tombol delete user
$('.delete-user').on('click', function(e){

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();
    
    //var href 
    const href = $(this).attr('href');

    Swal.fire({
                title: 'Are you sure?',
                text: "Want to delete this user data?",
                icon: 'warning',
                showCancelButton: true,
                confirmButtonColor: '#3085d6',
                cancelButtonColor: '#d33',
                confirmButtonText: 'Delete User!'
            }).then((result) => {
            if (result.isConfirmed) {
                document.location.href = href;
                Swal.fire(
                'Delete!',
                'Data has been deleted.',
                'success'
                )
            }
            })

});


// tombol delete groups
$('.delete-group').on('click', function (e) {

    // e = event
    // mematikan funtion href yang seharusnya berjalan jika di klick
    e.preventDefault();

    //var href 
    const href = $(this).attr('href');

    Swal.fire({
        title: 'Are you sure?',
        text: "Want to delete this group data?",
        icon: 'warning',
        showCancelButton: true,
        confirmButtonColor: '#3085d6',
        cancelButtonColor: '#d33',
        confirmButtonText: 'Delete Group!'
    }).then((result) => {
        if (result.isConfirmed) {
            document.location.href = href;
            Swal.fire(
                'Delete!',
                'Data has been deleted.',
                'success'
            )
        }
    })

});




// $('.notif').on('click', function(e){
//     Swal.fire({
//         title: 'Custom animation with Animate.css',
//         showClass: {
//         popup: 'animate__animated animate__fadeInDown'
//         },
//         hideClass: {
//         popup: 'animate__animated animate__fadeOutUp'}
// })
// });


// let table = new DataTable('#myTable');


// new DataTable('#dataTable');
// $('#dataTable').DataTable( {
//     // paging: false,
//     // scrollY: 400
// } );


// $(document).ready(function() {
//     $('#akunGuru').DataTable( {
//         "language": {
//                         "search": "Cari:",
//                         "lengthMenu": "Menampilkan _MENU_ data",
//                         "info": "Menampilkan _START_ sampai _END_ data dari _TOTAL_ data",
//                         "infoEmpty": "Tidak ada data yang ditampilkan",
//                         "infoFiltered": "(dari total _MAX_ data)",
//                         "zeroRecords": "Tidak ada hasil pencarian ditemukan",
//                         "paginate": {
//                             "first": "&laquo;",
//                             "last": "&raquo;",
//                             "next": "&rsaquo;",
//                             "previous": "&lsaquo;"
//                         }
//                     }
//     } );
// } );











