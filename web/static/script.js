document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Actualizar el estado de las reservas
    socket.on('booking_update', (data) => {
        for (const court in data) {
            for (const timeSlot in data[court]) {
                if (data[court][timeSlot] === 'booked') {
                    var cell = document.querySelector(`td[data-court="${court}"][data-time="${timeSlot}"]`);
                    if (cell) {
                        cell.style.backgroundColor = 'red';
                        cell.innerText = 'Booked';
                    }
                }
            }
        }
    });

    // Enviar una reserva
    document.querySelectorAll('td').forEach((cell) => {
        cell.addEventListener('click', (event) => {
            let court = cell.getAttribute('data-court');
            let time = cell.getAttribute('data-time');

            // Emitir el evento 'book'
            socket.emit('book', { 'facility': court, 'hour': time });
        });
    });
});
