import { Injectable } from '@angular/core';
import { environment } from '../../environments/environment';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class ApiService {
    private apiUrl = `${environment.apiUrl}`;

    constructor(private http: HttpClient) {}

    postUpdate(): Observable<any> {
      return this.http.post(`${this.apiUrl}/update`, null);
    }

    postArticle(text: string): Observable<any> {
      let payload = {
        "text": text,
        "size": 3
      }
      return this.http.post(`${this.apiUrl}/article`, payload);
    }
}
