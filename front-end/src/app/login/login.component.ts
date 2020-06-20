import { Component, OnInit } from '@angular/core';
import { Router, ActivatedRoute } from '@angular/router';
import { AuthenticationService } from '../authentication.service';

@Component({
    // moduleId: module.id.toString(),
    templateUrl: 'login.component.html'
})

export class LoginComponent implements OnInit {
    model: any = {};
    loading = false;
    returnUrl: string;
    username: string;

    constructor(
        private route: ActivatedRoute,
        private router: Router,
        private authenticationService: AuthenticationService
    ) { }

    ngOnInit() {
        this.returnUrl = this.route.snapshot.queryParams['returnUrl'] || '/';
    }

    login() {
        this.loading = true;
        this.authenticationService.login(this.model.username, this.model.password)
            .subscribe(
                data => { 
                    this.router.navigate([this.returnUrl]); 
                    let id : number = +localStorage.getItem('id');
                }
            );
    }

    register() {
        this.router.navigate(['register']);
    }
    
    logout() {
        this.authenticationService.logout()
    }
}