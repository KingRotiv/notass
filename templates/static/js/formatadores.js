var Formatadores = Formatadores || {}


// Formatar título
Formatadores.formatarTexto = function (texto) {
    var tagsToReplace = {
        "&": "&amp;",
        "<": "&lt;",
        ">": "&gt;"
    }
    function replaceTag(tag) {
        return tagsToReplace[tag] || tag;
    }

    function safe_tags_replace(str) {
        return str.replace(/[&<>]/g, replaceTag);
    }
    return safe_tags_replace(texto)
}


// Formatar data e hora 
Formatadores.formatarData = function (dataString) {
    const data = new Date(dataString)

    if (isNaN(data.getTime())) {
        return "Data inválida!"
    }

    const dia = data.getDate().toString().padStart(2, "0")
    const mes = (data.getMonth() + 1).toString().padStart(2, "0")
    const ano = data.getFullYear()

    const horas = data.getHours().toString().padStart(2, "0")
    const minutos = data.getMinutes().toString().padStart(2, "0")
    const segundos = data.getSeconds().toString().padStart(2, "0")

    return `${dia}/${mes}/${ano} ${horas}:${minutos}:${segundos}`
}


Formatadores.formatarDataParaTempoPassado = function (dataString) {
    const dataEntrada = new Date(dataString)
    const agora = new Date()

    // Verifica se a data é válida
    if (isNaN(dataEntrada.getTime())) {
        return "Data inválida!"
    }

    // Diferença em milissegundos
    const diferenca = agora.getTime() - dataEntrada.getTime();

    // Convertendo a diferença em diferentes unidades de tempo
    const minutos = Math.floor(diferenca / 60000)
    const horas = Math.floor(minutos / 60)
    const dias = Math.floor(horas / 24)
    const semanas = Math.floor(dias / 7)

    // Aproximação de meses e anos: considera meses como tendo 30 dias e anos como tendo 365 dias
    const meses = Math.floor(dias / 30)
    const anos = Math.floor(dias / 365)

    // Mensagem mais adequada
    let mensagem = ""
    if (anos > 0) {
        mensagem = `${anos} ano${anos > 1 ? "s" : ""}`
    } else if (meses > 0) {
        mensagem = `${meses} mes${meses > 1 ? "es" : ""}`
    } else if (dias > 0) {
        mensagem = `${dias} dia${dias > 1 ? "s" : ""}`
    } else if (horas > 0) {
        mensagem = `${horas} hora${horas > 1 ? "s" : ""}`
    } else if (minutos > 0) {
        mensagem = `${minutos} minuto${minutos > 1 ? "s" : ""}`
    } else {
        mensagem = "Agora"
    }

    return {
        minutos: minutos,
        dias: dias,
        semanas: semanas,
        meses: meses,
        anos: anos,
        mensagem: mensagem
    }
}
