
let map = L.map('map').setView([26.1054, 60.6405 ], 8); 
// 26.3054
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png').addTo(map);


// L.tileLayer('http://sgx.geodatenzentrum.de/wmts_topplus_open/tile/1.0.0/web/default/WEBMERCATOR/{z}/{y}/{x}.png', {
// 	attribution: 'Map data: &copy; <a href="http://www.govdata.de/dl-de/by-2-0">dl-de/by-2-0</a>'
// }).addTo(map);

// L.tileLayer('https://basemap.nationalmap.gov/arcgis/rest/services/USGSImageryTopo/MapServer/tile/{z}/{y}/{x}', {
// 	maxZoom: 20,
// 	attribution: 'Tiles courtesy of the <a href="https://usgs.gov/">U.S. Geological Survey</a>'
// }).addTo(map);



function style(feature) {  
    let fillColor;  
    if (
        feature.properties.SHAHRESTAN === 'سيريك' || 
        feature.properties.SHAHRESTAN === 'كنارك' || 
        feature.properties.SHAHRESTAN === 'چاه بهار' ||
        feature.properties.SHAHRESTAN === 'جاسك'
    ) {  
        fillColor = '#5a7796d3'; // lightblue  
    } else {  
        fillColor = '#779cc3d3'; // dark blue 
    }  
    
    return {  
        fillColor: fillColor,  
        weight: 2,  
        opacity: 1,  
        color: 'white',  
        fillOpacity: 0.7  
    };  
}

// fetch('/static/Geojson/makrangeojson/makranzone1.geojson')  
//     .then(response => response.json())  
//     .then(data => {  
//         L.geoJSON(data, { style: style }).addTo(map);  
//     });  


fetch('/static/Geojson/makrangeojson/makranzone1.geojson')
    .then(response => response.json())
    .then(data => {
        let geojsonLayer = L.geoJSON(data, {
            style: style,
            onEachFeature: function (feature, layer) {
                if (feature.properties && feature.properties.SHAHRESTAN) {
                    // محاسبه مرکز محدوده هندسی
                    let center = layer.getBounds().getCenter();

                    // ایجاد یک Tooltip در مرکز محدوده
                    let tooltip = L.tooltip({
                        permanent: true,
                        direction: "center",
                        className: "shahrestan-label"
                    }).setContent(feature.properties.SHAHRESTAN);

                    // اضافه کردن Tooltip در موقعیت مرکز محدوده
                    L.tooltip(center, { opacity: 0 }) // مارکر نامرئی برای نمایش متن
                        .bindTooltip(tooltip)
                        .addTo(map);
                }
            }
        }).addTo(map);

        function updateLabels() {
            let zoomLevel = map.getZoom();
            let tooltips = document.getElementsByClassName("shahrestan-label");

            for (let i = 0; i < tooltips.length; i++) {
                let tooltip = tooltips[i];
                tooltips[i].style.display = (zoomLevel < 7) ? "none" : "block";
                
                tooltip.style.background = "rgba(0, 0, 0, 0)";
                tooltip.style.padding = "5px";
                // tooltip.style.borderRadius = "5px";
                tooltip.style.fontWeight = "bold";
                tooltip.style.fontFamily = "Yekan";
                tooltip.style.fontSize = "20px";
                tooltip.style.boxShadow = "0px 0px 0px rgba(0, 0, 0, 0)";
                tooltip.style.border = "none";
                tooltip.style.color = "rgb(79, 78, 78)";
            }
        }

        map.on('zoomend', updateLabels);
        updateLabels();
    });


    
// fetch('/data/allpoints/')  // دریافت داده‌ها از API
// .then(response => response.json())
// .then(data => {
//     L.geoJSON(data, {
//         onEachFeature: function (feature, layer) {
//             layer.bindPopup(`<b>E${feature.geometry.coordinates[0]} N${feature.geometry.coordinates[1]}</b>`);
//             // ${feature.properties.name}
//         }
//     }).addTo(map);
// });
var smallIcon = L.icon({
    iconUrl: '/static/leaflet/images/marker-icon.png',  // آیکون پیش‌فرض
    iconSize: [15, 25],  // کوچک کردن اندازه آیکون (عرض، ارتفاع)
    // iconAnchor: [10, 30],  // محل قرارگیری آیکون نسبت به نقطه
    // popupAnchor: [0, -30]  // محل نمایش پاپ‌آپ نسبت به آیکون
});
// دریافت point_id از URL (مثلاً از آدرس /detail/<point_id>/)
const pointId = window.location.pathname.split('/').filter(Boolean).pop(); // گرفتن point_id از URL

// دریافت داده‌های نقطه خاص از API
fetch(`/data/data/point/${pointId}/`)
    .then(response => {
        console.log(response)
        if (!response.ok) {
            throw new Error('Point not found');
        }
        return response.json();
    })
    .then(data => {
        // تنظیم مرکز نقشه بر اساس مختصات نقطه
        const coords = data.geometry.coordinates; // فرض: [longitude, latitude]
        map.setView([coords[1], coords[0]], 8); // زوم بیشتر برای تمرکز روی نقطه

        // ایجاد مارکر برای نقطه خاص
        const marker = L.marker([coords[1], coords[0]], { icon: smallIcon }).addTo(map);

        // اضافه کردن پاپ‌آپ (مشابه استایل قبلی)
        marker.on('mouseover', function () {
            this.bindPopup(`
                <div style="direction: rtl; text-align: right; font-family: Yekan; font-size:16px">
                    <b style="color:#00008B">نام نقطه: </b><b style="color:#3b3b3b">${data.properties.name}</b> <br>
                    <b style="color:#00008B">موقعیت جغرافیایی: </b><b style="color:#3b3b3b">E${coords[0]} N${coords[1]}</b>
                </div>
            `).openPopup();
        });

        // بستن پاپ‌آپ هنگام خروج موس
        marker.on('mouseout', function () {
            this.closePopup();
        });
    })
    .catch(error => {
        console.error('Error fetching point data:', error);
        // نمایش پیام خطا روی نقشه یا صفحه
        map.setView([26.1054, 60.6405], 8); // بازگشت به نمای پیش‌فرض
        L.popup()
            .setLatLng([26.1054, 60.6405])
            .setContent('نقطه موردنظر یافت نشد.')
            .openOn(map);
    });