import { HttpClient, HttpHandler, HttpRequest } from '@angular/common/http';
import { Component, OnInit } from '@angular/core';
import * as XLSX from 'xlsx';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {
  excelData: any[] = [];

  public DIM: number = 0;
  public dailyMilk: number = 0;
  public milk305: number = 0;
  public fat: number = 0;
  public snf: number = 0;
  public density: number = 0;
  public protein: number = 0;
  public conductivity: number = 0;
  public ph: number = 0;
  public freezingPoint: number = 0;
  public salt: number = 0;
  public lactose: number = 0;

  ngOnInit(): void {}

  constructor(private http: HttpClient) {}

  onFileSelected(event: any): void {
    const file = event.target.files[0];
    if (file) {
      this.readExcelFile(file);
    }
  }

  readExcelFile(file: File): void {
    const fileReader = new FileReader();

    fileReader.onload = (e: any) => {
      const arrayBuffer = e.target.result;
      const data = new Uint8Array(arrayBuffer);
      const workbook = XLSX.read(data, { type: 'array' });

      // Assuming your Excel file contains only one sheet
      const sheetName = workbook.SheetNames[0];
      const worksheet = workbook.Sheets[sheetName];

      // Convert worksheet to JSON
      const jsonData = XLSX.utils.sheet_to_json(worksheet, { header: 1 });
      console.log(jsonData);

      //Send JSON data to the backend
      this.sendDataToBackend(jsonData);
    };

    fileReader.readAsArrayBuffer(file);

  }

  sendDataToBackend(data: any): void {
    // Use HttpClient to send data to your backend API
    const apiUrl = 'http://localhost:5000/predict';
    this.http.post(apiUrl, { excelData: data }).subscribe(
      (response) => {
        console.log('Excel data sent successfully:', response);
      },
      (error) => {
        console.error('Error sending Excel data:', error);
      }
    );
  }

  // function to get input data
  updateData(event: Event, type: string) {
    switch(type) {
      case "dim":
        this.DIM = Number((event.target as HTMLInputElement).value);
        console.log(this.DIM);
        break;
      case "avg":
        this.dailyMilk = Number((event.target as HTMLInputElement).value);
        console.log(this.dailyMilk);
        break;
      case "milk305":
        this.milk305 = Number((event.target as HTMLInputElement).value);
        console.log(this.milk305);
        break;
      case "fat":
        this.fat = Number((event.target as HTMLInputElement).value);
        console.log(this.fat);
        break;
      case "snf":
        this.snf = Number((event.target as HTMLInputElement).value);
        console.log(this.snf);
        break;
      case "density":
        this.density = Number((event.target as HTMLInputElement).value);
        console.log(this.density);
        break;
      case "protein":
        this.protein = Number((event.target as HTMLInputElement).value);
        console.log(this.protein);
        break;
      case "conductivity":
        this.conductivity = Number((event.target as HTMLInputElement).value);
        console.log(this.conductivity);
        break;
      case "ph":
        this.ph = Number((event.target as HTMLInputElement).value);
        console.log(this.ph);
        break;
      case "freezingPoint":
        this.freezingPoint = Number((event.target as HTMLInputElement).value);
        console.log(this.freezingPoint);
        break;
      case "salt":
        this.salt = Number((event.target as HTMLInputElement).value);
        console.log(this.salt);
        break;
      case "lactose":
        this.lactose = Number((event.target as HTMLInputElement).value);
        console.log(this.lactose);
        break;
      default:
        break;
    }


  }

  // this function send the input data to the backend
  public onSubmit () {
    console.log("data was submitted");
  }

}
