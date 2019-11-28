import { Component, OnInit } from '@angular/core';
import { FormBuilder, Validators } from '@angular/forms';
import { HttpClient } from '@angular/common/http';


@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'video-detection-client';

  public formGroup = this.fb.group({
    file: [null, Validators.required]
  });

  private fileName;

  constructor(private fb: FormBuilder, private http: HttpClient) { }

  public onFileChange(event) {
    const reader = new FileReader();

    if (event.target.files && event.target.files.length) {
      this.fileName = event.target.files[0].name;
      const [file] = event.target.files;
      reader.readAsDataURL(file);

      reader.onload = () => {
        this.formGroup.patchValue({
          file: (reader.result as string).split(',').pop()
        });
      };
    }
    console.log('this.for', this.formGroup);
  }

  public onSubmit(): void {
    this.http.post('http://localhost:5000/api/video', { data: this.formGroup.value }).subscribe(data => console.log('data', data));
  }
}
