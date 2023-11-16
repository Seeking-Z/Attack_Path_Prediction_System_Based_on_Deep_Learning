// 初始化图表
var cpuChart = new Chart(document.getElementById('cpuChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],  // 存储时间戳
        datasets: [{
            label: 'CPU使用率',
            data: [],
            borderColor: 'rgba(75, 192, 192, 1)',
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                display: false
            },
            y: {
                beginAtZero: true,
                suggestedMax: 100
            }
        }
    }
});

var memoryChart = new Chart(document.getElementById('memoryChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],
        datasets: [{
            label: '内存使用率',
            data: [],
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        }]
    },
    options: {
        scales: {
            x: {
                display: false
            },
            y: {
                beginAtZero: true,
                suggestedMax: 100
            }
        }
    }
});

var gpuChart = new Chart(document.getElementById('gpuChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],  // 存储时间戳
        datasets: [{
            label: 'GPU负载',
            data: [],  // 存储 GPU 负载数据
            borderColor: 'rgba(255, 159, 64, 1)',
            fill: false
        },
            {
                label: 'GPU内存使用率',
                data: [],  // 存储 GPU 内存使用率数据
                borderColor: 'rgba(54, 162, 235, 1)',
                fill: false
            }]
    },
    options: {
        scales: {
            x: {
                display: false
            },
            y: {
                beginAtZero: true,
                suggestedMax: 100
            }
        }
    }
});

var networkChart = new Chart(document.getElementById('networkChart').getContext('2d'), {
    type: 'line',
    data: {
        labels: [],  // 存储时间戳
        datasets: [{
            label: '网络发送字节数',
            data: [],  // 存储发送字节数数据
            borderColor: 'rgba(255, 99, 132, 1)',
            fill: false
        },
            {
                label: '网络接收字节数',
                data: [],  // 存储接收字节数数据
                borderColor: 'rgba(75, 192, 192, 1)',
                fill: false
            }]
    },
    options: {
        scales: {
            x: {
                display: false
            },
            y: {
                beginAtZero: true,
                suggestedMax: 100
            }
        }
    }
});

// 定时获取系统数据并更新图表
setInterval(function () {
    // 发送Ajax请求获取系统状态数据
    fetch('/api/systeminfo')
        .then(response => response.json())
        .then(data => {
            // 获取当前时间戳
            var now = new Date();
            var timestamp = now.toLocaleTimeString();

            // 更新CPU图表
            cpuChart.data.labels.push(timestamp);
            cpuChart.data.datasets[0].data.push(data.cpu_percent);
            cpuChart.update();

            // 更新内存图表
            memoryChart.data.labels.push(timestamp);
            memoryChart.data.datasets[0].data.push(data.memory_percent);
            memoryChart.update();

            // 更新GPU图表 - 如果有GPU信息的话
            if (data.gpu_info) {
                // 假设 GPU 数据是一个数组，包含负载和内存使用率
                data.gpu_info.forEach(gpu => {
                    gpuChart.data.labels.push(timestamp);
                    gpuChart.data.datasets[0].data.push(gpu.load); // GPU负载
                    gpuChart.data.datasets[1].data.push(gpu.memoryUtil); // GPU内存使用率
                });
                gpuChart.update();
            }

            // 更新网络图表 - 如果有网络信息的话
            if (data.bytes_sent && data.bytes_recv) {
                // 更新发送字节数
                networkChart.data.labels.push(timestamp);
                networkChart.data.datasets[0].data.push(data.bytes_sent);

                // 更新接收字节数
                networkChart.data.datasets[1].data.push(data.bytes_recv);

                networkChart.update();
            }
        });
}, 1000);  // 每秒更新一次
