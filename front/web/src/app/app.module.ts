import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/layout/header/header.component';
import { FooterComponent } from './components/layout/footer/footer.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { LoginComponent } from './components/auth/login/login.component';
import { MainComponent } from "./components/main/main.component";
import { LogoutComponent } from './components/auth/logout/logout.component';

import { RouterModule, Routes } from "@angular/router";
import { ReactiveFormsModule } from '@angular/forms';
import { CookieService} from "ngx-cookie-service";
import { CreateComponent } from './components/board/create/create.component';


const routes: Routes = [{
  path: 'login',
  component: LoginComponent
},{
  path: '',
  component: MainComponent
},{
  path: 'boards/create',
  component: CreateComponent
}];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    NavbarComponent,
    LoginComponent,
    MainComponent,
    LogoutComponent,
    CreateComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule
  ],
  providers: [CookieService],
  bootstrap: [AppComponent]
})
export class AppModule { }
