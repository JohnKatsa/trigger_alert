import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class UserDataService {
  users = []
  
  httpOptions = {
    headers: new HttpHeaders({ 'Content-Type': 'application/json' })
  };

  api = 'http://localhost:8000/';

  addUser(user) {
    this.users.push(user);
  }

  getUser(id : any) : Observable<any> {
    return this.http.get<any>(this.api+"users/"+id.toString()+'/');
  }

  createUser(user): Observable<any> {
    //return this.http.post(this.api+'users/',user,this.httpOptions);
    console.log(user)
    return this.http.post(this.api+'signup/', user, this.httpOptions);
  }

  validateUsername(username) : Observable<any> {
    return this.http.post(this.api+"validate_username/",{username:username},{responseType: 'text'});
  }

  getLinks(u_id : number): Observable<any> {
    return this.http.get(this.api+'links/user/?u_id=' + u_id.toString())
  }

  postLink(data : any): Observable<any> {
    return this.http.post(this.api+'links/user/?u_id=' + data.u_id.toString(), data, this.httpOptions);
  }
  
  constructor(
    private http: HttpClient
  ) { }
}