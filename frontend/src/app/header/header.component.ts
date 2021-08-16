import { Component, OnInit } from '@angular/core';
import { AuthenticationService } from '../authentication.service';

@Component({
  selector: 'app-header',
  templateUrl: './header.component.html',
  styleUrls: ['./header.component.scss'],
})
export class HeaderComponent implements OnInit {
  public label?: string;

  constructor(private authenticationService: AuthenticationService) {
    this.authenticationService.token$.subscribe((token) => {
      this.label = token !== null ? 'Admin Portal' : 'Admin Login';
    });
  }

  ngOnInit(): void {}
}
