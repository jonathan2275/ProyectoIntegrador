let imgs;

function searchPhoto() {
    if ($('#nombrep').val() == "") {
        alert("Indique nombre antes de buscar")
        return;
    }
    $('#btnBuscar').attr('disabled', true);
    $.ajax({
        url: "/searchPhoto?word=" + $('#nombrep').val(),
        type: 'GET',
        success: function(resp) {
            imgs = resp;
            let tbl = '<tr>';
            resp.forEach((element, index) => {
                if ((index + 1) % 8 == 0) {
                    tbl += `</tr>`;
                    tbl += `<tr>`;
                }
                tbl += `
                        <td>
                            <div class="custom-control custom-checkbox image-checkbox">
                                <input type="checkbox" class="custom-control-input" id="img${index}" checked>
                                <label class="custom-control-label" for="img${index}">
                                    <img src="${element}" width="150" height="150" alt="#" class="img-fluid">
                                </label>
                            </div>
                        </td>`;
            });
            tbl += `</tr>`;
            $('#tphoto').html(tbl);
            $('#totalP').html(resp.length);
            $('#btnBuscar').attr('disabled', false);
        },
        error: function(err) {
            console.log(err);
        }

    });
}

function saveProduct() {
    $.ajax({
        url: "/saveProduct?nombrep=" + $('#nombrep').val() + "&preciop=" + $('#preciop').val() + "&stockp=" + $('#stockp').val() + "&estadop=" + $('#estadop').val() + "&imgs=" + imgs,
        type: 'GET',
        success: function(resp) {
            console.log(resp);
            if (resp['ok'] == 200) {
                //alert("Ha sido guardado con exito");
                window.location.href = "/producto?msg=El%20Producto%20Ha%20sido%20guardado%20con%20exito&alert=alert-success";
            } else {
                //alert("Ha ocurrido algun error");
                window.location.href = "/producto?msg=Ha%20ocurrido%20algun%20error&alert=alert-danger";
            }

        },
        error: function(err) {
            console.log(err);
        }
    });
}

function updateProduct() {
    $.ajax({
        url: "/updateProduct?id=" + $('#didp').val() + "&nombrep=" + $('#dnombrep').val() + "&preciop=" + $('#dpreciop').val() + "&stockp=" + $('#dstockp').val() + "&estadop=" + $('#destadop').val(),
        type: 'GET',
        success: function(resp) {
            console.log(resp);
            if (resp['ok'] == 200) {
                //alert("Ha sido guardado con exito");
                window.location.href = "/producto?msg=El%20Producto%20Ha%20sido%20actualizado%20con%20exito&alert=alert-success";
            } else {
                //alert("Ha ocurrido algun error");
                window.location.href = "/producto?msg=Ha%20ocurrido%20algun%20error&alert=alert-danger";
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function detailsProduct(id) {
    $.ajax({
        url: "/detailsProduct?id=" + id,
        type: 'GET',
        success: function(resp) {
            console.log(resp.img[0][3]);
            $('#didp').val(id);
            $('#dnombrep').val(resp.producto[1]);
            $('#dpreciop').val(resp.producto[2]);
            $('#dstockp').val(resp.producto[3]);
            $('#destadop').val(resp.producto[4]);
            $('#dimgp').attr('src', resp.img[0][3]);
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function abrir() {
    $('#archivo').click();
    $('#archivo').change(function(e) {
        var files = $(this)[0].files[0].name;
        $('#path').val(files);
        if ($(this)[0].files && $(this)[0].files[0]) {
            var reader = new FileReader();
            reader.onloadend = function(e) {
                $('#imgsrc').attr('src', e.target.result);
                $('#imgsrc').show();
            }
            reader.readAsDataURL($(this)[0].files[0]);
            $('#divBusqueda').hide();
        }
    });
}

function buscar() {
    $('#divBusqueda').hide();
    $('#gifL1').show();
    $.ajax({
        url: "/predic?foto=" + $('#imgsrc').attr('src'),
        type: 'GET',
        success: function(resp) {
            console.log(resp);
            if (resp.producto) {
                $('#bidp').val(resp.producto[0]);
                $('#bnombrep').val(resp.producto[1]);
                $('#bpreciop').val(resp.producto[2]);
                $('#bstockp').val(resp.producto[3]);
                $('#bestadop').val(resp.producto[4]);
                $('#divBusqueda').show();
            } else {
                alert(err);
            }
            $('#gifL1').hide();
        },
        error: function(err) {
            $('#gifL1').hide();
            console.log(err);
        }
    });

}

function agregar() {
    $('#archivo').click();
};
let producto = [];

function cambio(event) {
    $('#gifL2').show();
    var input = event.target;
    var reader = new FileReader();
    reader.onload = function(e) {
        $.ajax({
            url: "/predic?foto=" + reader.result,
            type: 'GET',
            success: function(resp) {
                console.log(resp);
                if (!search(resp)) {
                    producto.push([resp.producto[0], resp.producto[1], resp.producto[2], 1]);
                }

                let app = '';
                $('#tfactura tbody tr').remove();
                producto.forEach((element, index) => {
                    app += `<tr> <td>${element[0]}</td> <td>${element[1]}</td> <td>${element[2]}</td> <td><input type="number" id="cantidad${index}" minlength="1" onchange="updateCant(${index})" value="${element[3]}"></td> <td><i class="fa fa-trash fa-2x" aria-hidden="true" onclick="eliminar(${element[0]})"></i></td> </tr>`;
                });
                calcular();
                $('#gifL2').hide();
                $('#tfactura').append(app);
            },
            error: function(err) {
                $('#gifL2').hide();
                console.log(err);
            }
        });
    }
    reader.readAsDataURL(input.files[0]);
}

function search(resp) {
    for (let index = 0; index < producto.length; index++) {
        if (producto[index][0] == resp.producto[0]) {
            producto[index][3] = producto[index][3] + 1;
            return true;
        }
    }
    return false;
}

function eliminar(e) {
    let app = '';
    $('#tfactura tbody tr').remove();
    producto.forEach((element, index) => {
        if (element[0] == e) {
            producto.splice(index, 1);
        }
    });
    producto.forEach((element, index) => {
        app += `<tr> <td>${element[0]}</td> <td>${element[1]}</td> <td>${element[2]}</td> <td><input type="number" id="cantidad${index}" minlength="1" onchange="updateCant(${index})" value="${element[3]}"></td> <td><i class="fa fa-trash fa-2x" aria-hidden="true" onclick="eliminar(${element[0]})"></i></td> </tr>`;
    });
    calcular();
    $('#tfactura').append(app);
}

function updateCant(i) {
    producto[i][3] = $(`#cantidad${i}`).val();
    calcular();
}

function calcular() {
    let total = 0.00;
    producto.forEach(element => {
        total += (element[2] * element[3]);
    });
    $('#totalf').text(total);
}

function saveFactura() {
    if ($('#nombref').val() == "" || $('#telefonof').val() == "" || $('#direccionf').val() == "" || producto.length == 0) {
        alert("Campos importantes");
        return;
    }
    $.ajax({
        url: "/saveFactura?nombref=" + $('#nombref').val() + "&cedulaf=" + $('#cedulaf').val() + "&telefonof=" + $('#telefonof').val() + "&direccionf=" + $('#direccionf').val() + "&totalf=" + $('#totalf').text() + "&estadof=" + $('#estadof').val() + "&produ=" + JSON.stringify(producto),
        type: 'GET',
        success: function(resp) {
            console.log(resp);
            if (resp['ok'] == 200) {
                //alert("Ha sido guardado con exito");
                window.location.href = "/facturacion?msg=La%20Factura%20Ha%20sido%20guardado%20con%20exito&alert=alert-success";
            } else {
                //alert("Ha ocurrido algun error");
                window.location.href = "/producto?msg=Ha%20ocurrido%20algun%20error&alert=alert-danger";
            }
        },
        error: function(err) {
            console.log(err);
        }
    });
}

function detailsFactura(id) {
    $.ajax({
        url: "/detailsFactura?id=" + id,
        type: 'GET',
        success: function(resp) {
            console.log(resp);
            $('#didf').val(id);
            $('#dcedulaf').val(resp.factura[1]);
            $('#dnombref').val(resp.factura[2]);
            $('#dtelefonof').val(resp.factura[3]);
            $('#ddireccionf').val(resp.factura[4]);
            $('#totald').text(resp.factura[5]);
            $('#destadof').val(resp.factura[6]);
            $('#dtfactura tbody tr').remove();
            let app;
            resp.produ.forEach(element => {
                app += `<tr> <td>${element[1]}</td> <td>${element[5]}</td> <td>${element[6]}</td> <td> ${element[3]}</td><td> ${element[6]*element[3]}</td> </tr>`;
            });
            $('#dtfactura').append(app);
        },
        error: function(err) {
            console.log(err);
        }
    });

}

function pdfFactura(id) {
    $.ajax({
        url: "/PDFfactura?id=" + id,
        type: 'GET',
        success: function(resp) {
            var blob = new Blob([resp]);
            var link = document.createElement('a');
            link.href = window.URL.createObjectURL(blob);
            link.download = "Factura.pdf";
            link.click();

        },
        error: function(err) {
            console.log(err);
        }
    });
}