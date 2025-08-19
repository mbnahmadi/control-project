
let map = L.map('map').setView([35, 50], 5); 
// 26.3054
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);
let markersLayer = L.markerClusterGroup().addTo(map);


let activeIcon = L.icon({
    iconUrl: '/static/images/location/green.png',   
    iconSize: [15, 15],               
});

let inactiveIcon = L.icon({
    iconUrl: '/static/images/location/red.png', 
    iconSize: [15, 15],
});


function loadLocations(url) {
    fetch(url)
        .then(response => response.json())
        .then(data => {
            markersLayer.clearLayers(); 

            data.forEach(loc => {
                let icon = loc.is_active_now ? activeIcon : inactiveIcon;

                let marker = L.marker([loc.lat, loc.lon], {icon: icon});
                markersLayer.addLayer(marker);


                marker.on('mouseover', function () {
                    this.bindPopup(`
                        <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                            <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${loc.company_name}</b> <br>
                            <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${loc.location}</b><br> 
                            <b style="color:#00008B">status: </b><b style="color:${loc.is_active_now ? 'green' : 'red'}">
                                ${loc.is_active_now ? 'Active' : 'Inactive'}
                            </b>            
                        </div>
                    `).openPopup();
                });
                marker.on('mouseout', function () {
                    this.closePopup();
                });
            });
        });
}

document.getElementById("active-locations-btn").addEventListener("click", function() {
    loadLocations("/projects/get-active-locations/");
});
document.getElementById("all-locations-btn").addEventListener("click", function() {
    loadLocations("/projects/get-all-locations/");
});




// company-location-daterange

let lastReportData = null;

const filterForm = document.getElementById('filter-form');

filterForm.addEventListener('submit', function(e) {
    e.preventDefault();  // جلوگیری از reload صفحه

    // گرفتن مقادیر فرم
    let company_name = document.getElementById('company').value;
    let location = document.getElementById('location').value;
    let start = document.getElementById('start-date').value;
    let end = document.getElementById('end-date').value;

    // ساخت query string
    let query = new URLSearchParams();
    if (company_name) query.append('company_name', company_name);
    if (location) query.append('location_name', location);
    if (start) query.append('start', start);
    if (end) query.append('end', end);
    // console.log(start)
    // console.log(end)
    // ارسال به API



    fetch('/projects/company-location-daterange/?' + query.toString())
    .then(res => res.json())
    .then(data => {
        lastReportData = data; 
        // console.log(lastReportData)
        markersLayer.clearLayers();  // پاک کردن مارکرهای قبلی

        data.forEach(company => {  // برای هر شرکت
            company.points.forEach(point => {  // برای هر نقطه
                let lat = point.lat;  // اگر تو API هست، یا باید اضافه بشه
                let lon = point.lon;  // اگر تو API هست
                // فرض کنیم lat/lon رو از پروژه داریم، در غیر اینصورت باید در API اضافه کنیم

                let icon = point.is_active_now ? activeIcon : inactiveIcon;

                let marker = L.marker([lat, lon], {icon: icon});
                markersLayer.addLayer(marker);

                marker.on('mouseover', function () {
                    this.bindPopup(`
                        <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                            <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${company.company_name}</b><br>
                            <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${point.location_name}</b><br>
                            
                             <b style="color:#00008B">start date: </b><b style="color:#3b3b3b">${point.start_date}</b><br> 
                             <b style="color:#00008B">end date: </b><b style="color:#3b3b3b">
                                 ${point.is_active_now ? '-' : `${point.end_date}` }
                             </b><br>
                             <b style="color:#00008B">status: </b><b style="color:${point.is_active_now ? 'green' : 'red'}">
                                 ${point.is_active_now ? 'Active' : 'Inactive'}
                             </b>            
                         </div>


                        </div>
                    `).openPopup();
                });
                marker.on('mouseout', function () {
                    this.closePopup();
                });
            });
        });
    });

});

document.getElementById("report").addEventListener("click", function() {

    if (!lastReportData) {
      alert("No report data available. Please run filter first!");
      return;
    }
    
    let tbody = document.getElementById("reportTableBody");
    tbody.innerHTML = "";
  
    lastReportData.forEach(company => {
      company.points.forEach((point, idx) => {
        let tr = document.createElement("tr");
        // {idx === 0 ? company.company_name : ""}
        tr.innerHTML = `
          <td class="border px-4 py-2">${company.company_name}</td>
          <td class="border px-4 py-2">${point.location_name}</td>
          <td class="border px-4 py-2">${point.start_date}</td>
          <td class="border px-4 py-2">${point.end_date ?? '-'}</td>
          <td class="border px-4 py-2">${point.days_format}</td>
          <td class="border px-4 py-2" style="color:${point.is_active_now ? 'green':'red'}">
          ${point.is_active_now ? 'Active' : 'Inactive'}
          
          <td class="border px-4 py-2">${point.active_days}</td>
          </td>
        `;
        tbody.appendChild(tr);
      });
      
            // <td class="border px-4 py-2">${company.total_days}</td>
            // <td class="border px-4 py-2">${company.total_location}</td>
    let summaryTr = document.createElement("tr");
    summaryTr.innerHTML = `
        <td class="border px-4 py-2 font-bold text-right" style="background-color: #D0FFBC" colspan="7">sumary</td>
        <td class="border px-4 py-2 font-bold" style="background-color: #D0FFBC">${company.total_days}</td>
        <td class="border px-4 py-2 font-bold" style="background-color: #D0FFBC">${company.total_location}</td>
    `;
    tbody.appendChild(summaryTr);
    });
    document.getElementById("map").classList.add("hidden");
    document.getElementById("reportModal").classList.remove("hidden");
  });
  
  // بستن popup
document.getElementById("closeModal").addEventListener("click", function() {
    document.getElementById("reportModal").classList.add("hidden");
    document.getElementById("map").classList.remove("hidden");

  });