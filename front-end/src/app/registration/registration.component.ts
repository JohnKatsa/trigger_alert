import { Component, OnInit } from '@angular/core';
import { UserDataService } from '../user-data.service';
import { FormBuilder } from '@angular/forms';
import { Router, ActivatedRoute } from '@angular/router';

@Component({
  selector: 'app-registration',
  templateUrl: './registration.component.html',
  styleUrls: ['./registration.component.css']
})
export class RegistrationComponent implements OnInit {
  myform;
  valid;

  constructor(
    private userService : UserDataService,
    private formBuilder : FormBuilder,
    private router: Router,
  ) {
    this.myform = this.formBuilder.group({
      username: '',
      email: '',
      password: '',
    });
   }

  ngOnInit() {
    this.valid = true;
  }

  onSubmit(data) {
    let user : any = {
      username : data.username,
      password : data.password,
      email : data.email,
    };
    console.log(user);
    this.userService.validateUsername(user.username).subscribe(data => {
      if (data == 'True'){
        this.userService.createUser(user).subscribe();
        this.valid = true;
        return this.router.navigate(['login/']);
      }
      else this.valid = false;
    })
  }
}