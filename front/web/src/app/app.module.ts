import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import { HttpClientModule } from '@angular/common/http';

import { AppComponent } from './app.component';
import { HeaderComponent } from './components/layout/header/header.component';
import { FooterComponent } from './components/layout/footer/footer.component';
import { NavbarComponent } from './components/layout/navbar/navbar.component';
import { LoginComponent } from './components/auth/login/login.component';

import { RouterModule, Routes } from "@angular/router";
import { ReactiveFormsModule } from '@angular/forms';

import { MainComponent } from './components/layout/main/main.component';
import { LogoutComponent } from './components/auth/logout/logout.component';

const routes: Routes = [{
  path: 'login',
  component: LoginComponent
},{
  path: '',
  component: MainComponent
}];

@NgModule({
  declarations: [
    AppComponent,
    HeaderComponent,
    FooterComponent,
    NavbarComponent,
    LoginComponent,
    MainComponent,
    LogoutComponent
  ],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot(routes),
    ReactiveFormsModule
  ],
  providers: [],
  bootstrap: [AppComponent]
})
export class AppModule { }
