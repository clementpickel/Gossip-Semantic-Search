import { Component } from '@angular/core';
import { ApiService } from './service/api.service';
import { ArticleDto } from './models/article.model';
import { catchError, throwError } from 'rxjs';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrl: './app.component.scss',
})
export class AppComponent {
  constructor(private apiService: ApiService) {}

  text = ''
  articles: ArticleDto[] = []

  onClickSearch() {
    this.apiService.postArticle(this.text).pipe(
      catchError(error => {
        console.error('Error occurred:', error);
        alert('Failed to fetch articles. Please try again later.')
        return throwError(() => error);
      })
    ).subscribe(
      res => {
        this.articles = res;
        console.log(res)
      }
    );
  }

  onClickUpdate() {
    this.apiService.postUpdate().pipe(
      catchError(error => {
        console.error('Error occurred:', error);
        alert('Failed to update. Please try again later.')
        return throwError(() => error);
      })
    ).subscribe(
      res => {
        // TODO
      }
    );
  }
}
