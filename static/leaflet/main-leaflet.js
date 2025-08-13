
let map = L.map('map').setView([35, 50], 5); 
// 26.3054
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);

fetch('/projects/get-active-locations/')  
    .then(res => res.json())
    .then(data => {
        data.forEach(loc => {
            let marker = L.marker([loc.lat, loc.lon]).addTo(map);

            marker.on('mouseover', function () {
                this.bindPopup(`
                    <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                        <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${loc.company_name}</b> <br>
                        <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${loc.location}</b><br>        
                    </div>
                `).openPopup();
            });

            marker.on('mouseout', function () {
                this.closePopup();
            });
        });
    });
