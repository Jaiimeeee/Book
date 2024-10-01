document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect('http://' + document.domain + ':' + location.port);

    // Actualizar el estado de las reservas cuando llega un evento 'booking_update'
    socket.on('booking_update', (data) => {
        console.log('Booking update received:', data);
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

    // Enviar una reserva al hacer clic en una celda de la tabla
    document.querySelectorAll('td').forEach((cell) => {
        cell.addEventListener('click', (event) => {
            const court = cell.getAttribute('data-court');
            const time = cell.getAttribute('data-time');
            if (court && time && cell.innerText === 'Book now') {
                socket.emit('book', { facility: court, hour: time });
            }
        });
    });
});
function bookCourt(court, time) {
    // Redirect to insert.html with the court and time as query parameters
    window.location.href = `/insert?court=${encodeURIComponent(court)}&time=${encodeURIComponent(time)}`;
}