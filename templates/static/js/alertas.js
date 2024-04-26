var Alertas = Alertas || {}


Alertas.customClassBootstrap = {
    confirmButton: "btn btn-primary m-1",
    cancelButton: "btn btn-secondary m-1",
    denyButton: "btn btn-danger m-1",
}


Alertas.swal = function () {
    const _Swal = Swal.mixin({
        allowOutsideClick: false,
        allowEscapeKey: false,
        buttonsStyling: false,
        customClass: Alertas.customClassBootstrap
    })
    return _Swal
}


Alertas.swalToast = function (options) {
    const { time = 2000, pos = "bottom-end" } = options
    const Toast = Swal.mixin({
        toast: true,
        position: pos,
        showConfirmButton: false,
        timer: time,
        timerProgressBar: true,
        buttonsStyling: false,
        customClass: Alertas.customClassBootstrap,
        didOpen: (toast) => {
            toast.onmouseenter = Swal.stopTimer;
            toast.onmouseleave = Swal.resumeTimer;
        }
    })
    return Toast
}