import { Component, OnInit } from '@angular/core';
import { BoardService } from '../../../services/board.service'
import { Board } from "../../../models/board";
import {Router} from "@angular/router";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isLoggedIn: boolean = false;
  boardList: Board[] = [];
  selectedBoard: Board;

  constructor(private boardService: BoardService,
              private authService: AuthService) { }

  getBoardList() {
    this.boardService.getBoardList()
      .subscribe((data: Board[]) => {
        this.boardList = data;
      })
  }

  onSelected(board: Board) {
    this.selectedBoard = board;
  }

  ngOnInit() {
    this.isLoggedIn = this.authService.isLoggedIn();

    this.getBoardList();
  }
}
