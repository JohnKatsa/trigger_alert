import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { map } from 'rxjs/operators';
import { Observable }  from 'rxjs';

const httpOptions = {
  headers: new HttpHeaders({ 'Content-Type': 'application/json' })
};

@Injectable({ providedIn: 'root' })
export class AuthenticationService {
    constructor(private http: HttpClient) { }

    login(username: string, password: string): Observable<any> {
        let ln = { "username": username, "password": password };
        let token = {"token":""};
        console.log(ln);
        return this.http.post<any>("http://localhost:8000/api/token/", ln, {responseType: 'text' as 'json'})
            .pipe(map(token => { 
                let a = JSON.parse(token).token;
                console.log(JSON.parse(token).token)
                localStorage.setItem('token', "token "+a);
                localStorage.setItem('username',ln.username);
                
                const token_parts = token.split(/\./);
                // console.log(token_parts)
                const token_decoded = JSON.parse(window.atob(token_parts[1]));
                localStorage.setItem('id',token_decoded.user_id);
                console.log(token_decoded);
                return token;
            }));        
    }

    logout(): void {
        // remove token from local storage to log user out
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        console.log("ok")
    }
}