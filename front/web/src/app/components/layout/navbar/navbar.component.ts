import { Component, OnInit } from '@angular/core';
import { BoardService } from '../../../services/board.service'
import { Board } from "../../../models/board";
import {Router} from "@angular/router";

@Component({
  selector: 'app-navbar',
  templateUrl: './navbar.component.html',
  styleUrls: ['./navbar.component.css']
})
export class NavbarComponent implements OnInit {
  boardList: Board[] = [];
  selectedBoard: Board;

  constructor(private boardservice: BoardService, private router: Router) { }

  getBoardList() {
    this.boardservice.getBoardList()
      .subscribe((data: Board[]) => {
        this.boardList = data;
      })
  }

  onSelected(board: Board) {
    this.selectedBoard = board;
  }

  ngOnInit() {
    this.getBoardList();
  }
}
