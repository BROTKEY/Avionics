class Tables {
  BNO;

  constructor() {
    const launch = (document.getElementById("launch").onclick = () => {
      axios.get("http://localhost:5000/launch");
    });

    const bno_ = document.getElementById("BNO").getContext("2d");
    this.BNO = new Chart(bno_, {
      type: "line",
      data: {
        labels: this.labels,
        datasets: [
          {
            label: "x",
            data: this.x,
            backgroundColor: ["rgba(255, 0, 0, 0.2)"],
            borderColor: ["rgba(255, 0, 0, 1)"],
            borderWidth: 1,
          },
          {
            label: "y",
            data: this.y,
            backgroundColor: ["rgba(0, 255, 0, 0.2)"],
            borderColor: ["rgba(0, 255, 0, 1)"],
            borderWidth: 1,
          },
          {
            label: "z",
            data: this.z,
            backgroundColor: ["rgba(0, 0, 255, 0.2)"],
            borderColor: ["rgba(0, 0, 255, 1)"],
            borderWidth: 1,
          },
        ],
      },
      options: {
        elements: {
          point: {
            radius: 0,
          },
        },
        animation: {
          duration: 0,
        },
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "BNO",
          },
        },
      },
    });

    const bmp_ = document.getElementById("BMP").getContext("2d");
    this.BMP = new Chart(bmp_, {
      type: "line",
      data: {
        labels: this.labels,
        datasets: [
          {
            label: "altitude",
            data: this.x,
            backgroundColor: ["rgba(255, 0, 0, 0.2)"],
            borderColor: ["rgba(255, 0, 0, 1)"],
            borderWidth: 1,
          },
          {
            label: "pressure",
            data: this.y,
            backgroundColor: ["rgba(0, 255, 0, 0.2)"],
            borderColor: ["rgba(0, 255, 0, 1)"],
            borderWidth: 1,
          },
          {
            label: "temperature",
            data: this.z,
            backgroundColor: ["rgba(0, 0, 255, 0.2)"],
            borderColor: ["rgba(0, 0, 255, 1)"],
            borderWidth: 1,
          },
        ],
      },
      options: {
        elements: {
          point: {
            radius: 0,
          },
        },
        animation: {
          duration: 0,
        },
        responsive: true,
        plugins: {
          legend: {
            position: "top",
          },
          title: {
            display: true,
            text: "BMP",
          },
        },
      },
    });
  }

  async update() {
    var response = await axios.get("http://localhost:5000/");
    var BNO = response.data[1];
    var BMP = response.data[0];
    this.BNO.data.labels = BNO.map((x) => x[1]);
    this.BNO.data.datasets[0].data = BNO.map((i) => i[0][0]);
    this.BNO.data.datasets[1].data = BNO.map((i) => i[0][1]);
    this.BNO.data.datasets[2].data = BNO.map((i) => i[0][2]);
    this.BNO.update();
    this.BMP.data.labels = BMP.map((x) => x[1]);
    this.BMP.data.datasets[0].data = BMP.map((i) => i[0][0]);
    this.BMP.data.datasets[1].data = BMP.map((i) => i[0][1]);
    this.BMP.data.datasets[2].data = BMP.map((i) => i[0][2]);
    this.BMP.update();
    setTimeout(this.update(), 1000);
  }
}

tables = new Tables();
tables.update();
