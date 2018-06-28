import { Component, OnInit } from '@angular/core';
import { BoardService } from '../../../services/board.service'
import {Board, NavBoard} from "../../../models/board";
import {Router} from "@angular/router";
import {AuthService} from "../../../services/auth.service";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  isLoggedIn: boolean = false;
  boardList: NavBoard[] = [];
  selectedBoard: NavBoard;

  constructor(private boardService: BoardService,
              private authService: AuthService,
              private router: Router) { }

  getNavBoardList() {
    this.boardService.getNavBoardList()
      .subscribe((data: NavBoard[]) => {
        this.boardList = data;
      })
  }

  onSelected(board: Board) {
    this.selectedBoard = board;
    this.router.navigate([`/boards/${board.id}/posts`])
  }

  ngOnInit() {
    this.isLoggedIn = this.authService.isLoggedIn();

    this.getNavBoardList();
  }
}
