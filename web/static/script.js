document.addEventListener('DOMContentLoaded', () => {
    var socket = io.connect(window.location.protocol + '//' + document.domain + ':' + location.port);

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

    // Function to get query parameters from URL
    function getQueryParam(param) {
        const urlParams = new URLSearchParams(window.location.search);
        return urlParams.get(param);
    }

    // Add event listener to the confirm button
    document.querySelector("#confirm").addEventListener('click', function() {
        const court = getQueryParam('court');
        const time = getQueryParam('time');
        const id_number = document.getElementById('id_number').value; // Get the value from the input field
        console.log('Court:', court, 'Time:', time, 'ID Number:', id_number); // Debugging

        if (court && time && id_number) {
            // Emit booking event
            socket.emit('book', { facility: court, hour: time, id_number: id_number });
        } else {
            alert('Please fill out all fields before confirming the booking.');
        }
    });
});

