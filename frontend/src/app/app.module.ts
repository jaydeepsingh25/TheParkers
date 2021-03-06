import { NgModule } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';

import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { IonicModule } from '@ionic/angular';
import { AngularFireModule } from '@angular/fire/compat';

import { environment } from "../environments/environment.dev";
import { FirebaseService, GuardService , AuthService, LocalStorageService, PreLoaderService, HttpInterceptorService} from './services'
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatIconModule } from '@angular/material/icon';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatDatepickerModule } from '@angular/material/datepicker';
import {MatExpansionModule} from '@angular/material/expansion';
import {MatCheckboxModule} from '@angular/material/checkbox';
import { BookingService } from './services'
import { MatTableModule } from '@angular/material/table' 

import { AgmCoreModule, GoogleMapsScriptProtocol } from '@agm/core';
import { MatGoogleMapsAutocompleteModule } from '@angular-material-extensions/google-maps-autocomplete';


import { SETTINGS as AUTH_SETTINGS } from '@angular/fire/compat/auth';
import { LANGUAGE_CODE } from '@angular/fire/compat/auth';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { FormsModule, ReactiveFormsModule } from '@angular/forms';
import { MatNativeDateModule } from '@angular/material/core';
import { SearchParkingComponent } from './components/search-parking/search-parking.component';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { DashboardComponent } from './components/dashboard/dashboard.component';
import { HomeComponent } from './components/home/home.component';
import { ParkingsListComponent } from './components/parkings-list/parkings-list.component';
import { ParkersHeaderComponent } from './components/parkers-header/parkers-header.component';
import { ParkingSpaceDescComponent } from './components/parking-space-desc/parking-space-desc.component';
import { AddParkingComponent } from './components/add-parking/add-parking.component';
import { BookingComponent } from './components/booking/booking.component';
import { ParkingsService } from './services/parkings/parkings.service';
import { BookingsListComponent } from './components/bookings-list/bookings-list.component';
import { BookingDescComponent } from './components/booking-desc/booking-desc.component';


@NgModule({
  declarations: [
    SearchParkingComponent,
    DashboardComponent,
    AppComponent,
    HomeComponent,
    ParkingsListComponent,
    ParkersHeaderComponent,
    ParkingSpaceDescComponent,
	  BookingComponent,
    AddParkingComponent,
    BookingsListComponent,
    BookingDescComponent
  ],
  entryComponents: [BookingComponent],
  imports: [
    BrowserModule,
    AppRoutingModule,
    HttpClientModule,
    IonicModule.forRoot({
      animated: true
    }),
    AgmCoreModule.forRoot({
      protocol: GoogleMapsScriptProtocol.HTTPS,
      apiKey: environment.googleMapsApiKey,
      libraries: ['places']
    }),
    AngularFireModule.initializeApp(environment.firebaseConfig),
    FormsModule,
    ReactiveFormsModule,
    MatNativeDateModule,
    BrowserAnimationsModule,
    MatFormFieldModule,
    MatInputModule,
    MatIconModule,
    MatCardModule,
    MatButtonModule,
    MatDatepickerModule,
    MatExpansionModule,
    MatGoogleMapsAutocompleteModule,
    MatTableModule,
    MatCheckboxModule
  ],
  providers: [
    { provide: AUTH_SETTINGS, useValue: { appVerificationDisabledForTesting: false } },
    { provide: LANGUAGE_CODE, useValue: 'fr' },
    { provide: HTTP_INTERCEPTORS, useClass: HttpInterceptorService, multi: true },
    AuthService,
    FirebaseService, 
    GuardService,
    LocalStorageService,
    PreLoaderService,
	  BookingService,
    ParkingsService
  ],
  bootstrap: [AppComponent]
})
export class AppModule { }