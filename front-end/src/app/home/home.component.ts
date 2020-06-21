import { Component, OnInit } from '@angular/core';
import { UserDataService } from '../user-data.service';
import { AuthenticationService } from '../authentication.service';
import { Router } from '@angular/router';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.css']
})
export class HomeComponent implements OnInit {

  model : any = {}
  links;

  constructor(private userService : UserDataService,
              private authenticationService : AuthenticationService,
              private router: Router) { }

  ngOnInit(): void {
    this.getLinks()
    setInterval(() => this.getLinks(), 5000);
  }

  getLinks(): void {
    this.userService.getLinks(+localStorage.getItem("id")).subscribe(data => {
      this.links = data
      console.log(data)
      console.log(this.links)
      console.log(+localStorage.getItem("id"))
    })
  }

  postLink(): void {
    let data = {
      url : (document.getElementById("link") as HTMLInputElement).value,
      page_id : (document.getElementById("pages") as HTMLInputElement).value || null,
      is_multi_page : (document.getElementById("has_pages") as HTMLInputElement).checked,
      u_id : +localStorage.getItem("id")
    }

    console.log(data)

    this.userService.postLink(data).subscribe(data => {
      console.log(data);
      this.getLinks();
    });

    (document.getElementById("link") as HTMLInputElement).value = ""
  }

  signout(): void {
    this.authenticationService.logout();
    this.router.navigate(['login/']);
  }

}
