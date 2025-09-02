
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

            data.features.forEach(f => {
                const geom = f.geometry;
                const props = f.properties;
                // console.log(loc)
                let icon = props.is_active_now ? activeIcon : inactiveIcon;
                
                if (geom.type === 'Point') {
                    let marker = L.marker([geom.coordinates[1], geom.coordinates[0]], {icon: icon});
                    markersLayer.addLayer(marker);
               
                    marker.on('mouseover', function () {
                        this.bindPopup(`
                            <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                                <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${props.company_name}</b> <br>
                                <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${props.location}</b><br> 
                                <b style="color:#00008B">status: </b><b style="color:${props.is_active_now ? 'green' : 'red'}">
                                    ${props.is_active_now ? 'Active' : 'Inactive'}
                                </b>            
                            </div>
                        `).openPopup();
                    });
                    marker.on('mouseout', function () {
                        this.closePopup();
                    });

                    // دانلود PDF با کلیک (فقط برای نقاط فعال)
                    if (props.is_active_now) {
                        marker.on('click', function () {
                            window.location.href = `/projects/download-pdf/${props.pk}/`;
                        });
                    }
                }
                else if (geom.type === 'LineString') {
                    let latlngs = geom.coordinates.map(c => [c[1], c[0]]);
                    let polyline = L.polyline(latlngs, { color: props.is_active_now ? 'green' : 'red' });
                    markersLayer.addLayer(polyline);
                    polyline.on('mouseover', function () {
                        this.bindPopup(`
                            <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                                <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${props.company_name}</b> <br>
                                <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${props.location}</b><br> 
                                <b style="color:#00008B">status: </b><b style="color:${props.is_active_now ? 'green' : 'red'}">
                                    ${props.is_active_now ? 'Active' : 'Inactive'}
                                </b>            
                            </div>
                        `).openPopup();
                    });
                    polyline.on('mouseout', function () {
                        this.closePopup();
                    });
                    if (props.is_active_now) {
                        polyline.on('click', function () {
                            window.location.href = `/projects/download-pdf/${props.pk}/`;
                        });
                    }
                }
            });
        });
}

document.getElementById("active-locations-btn").addEventListener("click", function() {
    loadLocations("/projects/get-active-locations/");
});

document.getElementById("all-locations-btn").addEventListener("click", function() {
    loadLocations("/projects/get-all-locations/");
});

document.getElementById("all-routes-btn").addEventListener("click", function() {
    loadLocations("/projects/get-all-routes/");
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

        data.forEach(company => {  
            console.log('company', company)
            company.detail.forEach(location => {  // برای هر نقطه
                // console.log('location', location)
                // const geom = f.geometry;
                // const props = f.properties;
                if (location.geometry.type === 'Point'){
                    let lat = location.geometry.coordinates[1];  // اگر تو API هست، یا باید اضافه بشه
                    let lon = location.geometry.coordinates[0];  // اگر تو API هست
                    // فرض کنیم lat/lon رو از پروژه داریم، در غیر اینصورت باید در API اضافه کنیم
                    // console.log('lat', lat)
                    // console.log('lon', lon)
               
                    let icon = location.is_active_now ? activeIcon : inactiveIcon;

                    let marker = L.marker([lat, lon], {icon: icon});
                    markersLayer.addLayer(marker);

                    marker.on('mouseover', function () {
                        this.bindPopup(`
                            <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                                <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${company.company_name}</b><br>
                                <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${location.location_name}</b><br>
                                
                                <b style="color:#00008B">start date: </b><b style="color:#3b3b3b">${location.start_date}</b><br> 
                                <b style="color:#00008B">end date: </b><b style="color:#3b3b3b">
                                    ${location.is_active_now ? '-' : `${location.end_date}` }
                                </b><br>
                                <b style="color:#00008B">status: </b><b style="color:${location.is_active_now ? 'green' : 'red'}">
                                    ${location.is_active_now ? 'Active' : 'Inactive'}
                                </b>            
                            </div>


                            </div>
                        `).openPopup();
                    });
                    marker.on('mouseout', function () {
                        this.closePopup();
                    });
                    
                    // دانلود PDF با کلیک (فقط برای نقاط فعال)
                    if (location.is_active_now) {
                        marker.on('click', function () {
                            window.location.href = `/projects/download-pdf/${location.pk}/`;
                        });
                    }
                }
                else if (location.geometry.type === 'LineString'){
                    let latlngs = location.geometry.coordinates.map(c => [c[1], c[0]]);
                    console.log('latlngs', latlngs)
                    let polyline = L.polyline(latlngs, { color: location.is_active_now ? 'green' : 'red' });
                    markersLayer.addLayer(polyline);
                    polyline.on('mouseover', function () {
                        this.bindPopup(`
                            <div style="direction: ltr; text-align: left; font-family: sans-serif; font-size:16px">
                                <b style="color:#00008B">Company: </b><b style="color:#3b3b3b">${company.company_name}</b><br>
                                <b style="color:#00008B">Location: </b><b style="color:#3b3b3b">${location.location_name}</b><br>
                                
                                <b style="color:#00008B">start date: </b><b style="color:#3b3b3b">${location.start_date}</b><br> 
                                <b style="color:#00008B">end date: </b><b style="color:#3b3b3b">
                                    ${location.is_active_now ? '-' : `${location.end_date}` }
                                </b><br>
                                <b style="color:#00008B">status: </b><b style="color:${location.is_active_now ? 'green' : 'red'}">
                                    ${location.is_active_now ? 'Active' : 'Inactive'}
                                </b>            
                            </div>


                            </div>
                        `).openPopup();
                    });
                    polyline.on('mouseout', function () {
                        this.closePopup();
                    });
                    if (location.is_active_now) {
                        polyline.on('click', function () {
                            window.location.href = `/projects/download-pdf/${location.pk}/`;
                        });
                    }
                }
                
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


