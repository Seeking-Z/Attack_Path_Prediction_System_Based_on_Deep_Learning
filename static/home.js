function getSystemInfo() {
    fetch('/api/systeminfo')
        .then(response => response.json())
        .then(data => {
            document.getElementById('cpuUsage').innerText = `${data.cpu_percent}%`;
            document.getElementById('memoryUsage').innerText = `${data.memory_percent}%`;
            document.getElementById('sent').innerText = `${data.bytes_sent} KB/S`;
            document.getElementById('recv').innerText = `${data.bytes_recv} KB/S`;
        })
        .catch(error => console.error('Error:', error));
}

setInterval(getSystemInfo, 1000); // 每秒更新一次系统信息
