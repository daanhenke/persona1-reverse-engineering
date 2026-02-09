
undefined4 adv_textbox_process(void)

{
  undefined1 *puVar1;
  uint *puVar2;
  char *pcVar3;
  char cVar4;
  short sVar5;
  uint uVar6;
  int iVar7;
  int iVar8;
  undefined2 *puVar9;
  uint uVar10;
  uint uVar11;
  byte bVar12;
  ushort uVar13;
  int iVar14;
  undefined *puVar15;
  char *pcVar16;
  ushort uVar17;
  ushort *puVar18;
  ushort *puVar19;
  ushort *puVar20;
  undefined1 auStack_18 [4];
  undefined4 uStack_14;
  
  puVar1 = auStack_18 + 3;
  uVar6 = (uint)puVar1 & 3;
  *(uint *)(puVar1 + -uVar6) =
       *(uint *)(puVar1 + -uVar6) & -1 << (uVar6 + 1) * 8 | DAT_ADV_BIN__800643c8 >> (3 - uVar6) * 8
  ;
  auStack_18 = (undefined1  [4])DAT_ADV_BIN__800643c8;
  uVar6 = (int)&uStack_14 + 3U & 3;
  puVar2 = (uint *)(((int)&uStack_14 + 3U) - uVar6);
  *puVar2 = *puVar2 & -1 << (uVar6 + 1) * 8 | DAT_ADV_BIN__800643cc >> (3 - uVar6) * 8;
  uStack_14 = DAT_ADV_BIN__800643cc;
  bVar12 = 0;
  uVar6 = 0;
  do {
    (&DAT_800eb14c)[uVar6] = 0;
    bVar12 = bVar12 + 1;
    uVar6 = (uint)bVar12;
  } while (bVar12 < 0x40);
  puVar19 = textbox_text_ptr;
  if ((textbox_state_flags & 1) != 0) {
    puVar19 = DAT_800e1e5c;
  }
  if ((textbox_state_flags & 0x8000) != 0) {
    return 1;
  }
  uVar6 = 0;
  if ((textbox_state_flags & 0x80000) != 0) {
    textbox_state_flags = textbox_state_flags ^ 0x80000 | 1;
    DAT_800e1e81 = 5;
    puVar18 = (ushort *)(&DAT_8004904a + ((byte)*textbox_text_ptr - 1) * 0x14);
LAB_ADV_BIN__80067728:
    DAT_800e1e56 = DAT_800e1e56 % 0x3c;
    uVar10 = textbox_state_flags;
    if ((textbox_state_flags & 4) == 0) {
      if (DAT_800e1e56 == 0x1e) {
        uVar10 = textbox_state_flags | 4;
      }
    }
    else if (((uint)DAT_800e1e56 % 0xf == 0) &&
            (uVar10 = textbox_state_flags ^ 0x100000, (textbox_state_flags & 0x100000) == 0)) {
      uVar10 = textbox_state_flags | 2;
    }
    textbox_state_flags = uVar10;
    if (0x7f < uVar6) {
      uVar17 = *puVar18;
      puVar18 = (ushort *)((int)puVar18 + 1);
      uVar6 = (uint)(byte)uVar17 | (uVar6 & 7) << 8;
    }
    adv_draw_jp_glyph((DAT_800e1e56 + 1 & 0xf) << 2 | 0x3c0,
                      (int)(((DAT_800e1e56 + 1 & 0xfffffff0) + 0x100) * 0x10000) >> 0x10,uVar6);
    adv_textbox_update_cursor(DAT_800e1e56,uVar6);
    DAT_800e1e56 = DAT_800e1e56 + 1;
    DAT_800e1e52 = DAT_800e1e54;
    if ((textbox_state_flags & 1) == 0) {
      textbox_text_ptr = puVar18;
      return 0;
    }
    DAT_800e1e81 = DAT_800e1e81 - 1;
    puVar20 = puVar18;
    if (DAT_800e1e81 == 0) {
      uVar6 = textbox_state_flags ^ 1;
      if ((textbox_state_flags & 0x40000) == 0) {
LAB_ADV_BIN__800678c0:
        puVar20 = (ushort *)((int)textbox_text_ptr + 1);
        textbox_state_flags = uVar6;
      }
      else {
LAB_ADV_BIN__800678a8:
        textbox_state_flags = textbox_state_flags ^ 0x40000;
        uVar6 = 0x80000;
LAB_ADV_BIN__800678b0:
        puVar20 = puVar18;
        textbox_state_flags = textbox_state_flags | uVar6;
      }
    }
    goto switchD_ADV_BIN__80066e7c_default;
  }
  puVar20 = puVar19;
  if ((textbox_state_flags & 0x20000) == 0) {
    if (DAT_800e1e50 != 0) {
      DAT_800e1e50 = DAT_800e1e50 + -1;
      return 0;
    }
    if ((textbox_state_flags & 8) == 0) {
      if ((DAT_800e1e52 != 0) && (DAT_800dc000 == 0)) {
        DAT_800e1e52 = DAT_800e1e52 + -1;
        return 0;
      }
    }
    else {
      if (DAT_800dc004 == 0) goto switchD_ADV_BIN__80066e7c_default;
      textbox_state_flags = textbox_state_flags & 0xfffffff7;
      adv_textbox_copy_state(auStack_18,&DAT_ADV_BIN__800b1a18);
      adv_textbox_clear_scroll(0);
    }
LAB_ADV_BIN__80066c50:
    uVar10 = DAT_801f2678;
    if ((textbox_state_flags & 2) == 0) {
      if ((textbox_state_flags & 0x4000) != 0) goto LAB_ADV_BIN__80066cf0;
      uVar6 = (uint)(byte)*puVar19;
      puVar18 = (ushort *)((int)puVar19 + 1);
      if (uVar6 != 0xff) goto LAB_ADV_BIN__80067728;
      bVar12 = *(byte *)puVar18;
      puVar18 = puVar19 + 1;
      puVar20 = puVar18;
      switch(bVar12) {
      case 1:
        if ((textbox_state_flags & 1) == 0) goto LAB_ADV_BIN__80066f24;
        if ((textbox_state_flags & 0x10000) != 0) {
          textbox_state_flags = textbox_state_flags | 0x20000;
          adv_textbox_setup_scroll(0,&LAB_ADV_BIN__800b1a30,0x20,0x1e2,0xb,1);
          adv_setup_sprite_obj(&PTR_DAT_ADV_BIN__800b1ab4_ADV_BIN__800b1b34,0x2e,0x1e,0x28,0xb4);
          adv_show_window(0x2e,1);
        }
        if ((textbox_state_flags & 0x40000) != 0) goto LAB_ADV_BIN__800678a8;
        uVar6 = textbox_state_flags & 0xfff6fffe;
        goto LAB_ADV_BIN__800678c0;
      case 2:
        textbox_state_flags = textbox_state_flags | 8;
        adv_textbox_setup_scroll(0,&LAB_ADV_BIN__800b1a30,0x20,0x1e2,0xb,1);
        goto switchD_ADV_BIN__80066e7c_default;
      case 3:
        DAT_800e1e56 = (short)((DAT_800e1e56 + 0xf) / 0xf) * 0xf +
                       (short)((DAT_800e1e56 + 0xf) / 0x3c) * -0x3c;
        uVar6 = textbox_state_flags | 2;
        if ((((textbox_state_flags & 4) == 0) ||
            (uVar10 = textbox_state_flags & 4, textbox_state_flags = uVar6, uVar10 == 0)) &&
           (0x1d < DAT_800e1e56)) {
          textbox_state_flags = textbox_state_flags | 4;
        }
        uVar6 = 0x100000;
        goto LAB_ADV_BIN__800678b0;
      case 4:
        iVar7 = 0xe;
        puVar9 = &DAT_ADV_BIN__800bca70;
        DAT_ADV_BIN__800b8f06 = 0;
        DAT_800e1e56 = 0;
        do {
          *puVar9 = 0;
          iVar7 = iVar7 + -1;
          puVar9 = puVar9 + -1;
        } while (-1 < iVar7);
        iVar8 = 0;
        iVar7 = 0x1e;
        do {
          *(undefined2 *)(&DAT_ADV_BIN__800bca54 + iVar7) = 0;
          iVar8 = iVar8 + 1;
          iVar7 = iVar7 + 2;
        } while (iVar8 < 0xf);
        iVar8 = 0;
        iVar7 = 0x3c;
        do {
          *(undefined2 *)(&DAT_ADV_BIN__800bca54 + iVar7) = 0;
          iVar8 = iVar8 + 1;
          iVar7 = iVar7 + 2;
        } while (iVar8 < 0xf);
        iVar8 = 0;
        iVar7 = 0x5a;
        do {
          *(undefined2 *)(&DAT_ADV_BIN__800bca54 + iVar7) = 0;
          iVar8 = iVar8 + 1;
          iVar7 = iVar7 + 2;
        } while (iVar8 < 0xf);
        uVar6 = 0xfffffffb;
        goto LAB_ADV_BIN__800670b0;
      case 5:
        DAT_800e1e50 = (ushort)(byte)*puVar18 + (ushort)*(byte *)((int)puVar19 + 3) * 0x100;
        puVar20 = puVar19 + 2;
        goto switchD_ADV_BIN__80066e7c_default;
      case 6:
        textbox_state_flags = (textbox_state_flags & 0xfc0f) + (uint)(byte)*puVar18 * 0x10;
        puVar20 = (ushort *)((int)puVar19 + 3);
        goto switchD_ADV_BIN__80066e7c_default;
      case 7:
        bVar12 = (byte)*puVar18;
        puVar15 = &DAT_8004904a;
        goto LAB_ADV_BIN__80067230;
      case 8:
        DAT_800e1e81 = 8;
        puVar15 = &UNK_8004428a;
        iVar7 = (uint)(byte)*puVar18 * 0x28;
        break;
      case 9:
        textbox_text_ptr = (ushort *)((int)puVar19 + 3);
        puVar15 = &DAT_8004440c;
        iVar7 = (uint)*puVar18 << 5;
        goto LAB_ADV_BIN__800671f4;
      case 10:
        DAT_800e1e81 = 10;
        puVar15 = &UNK_80047d44;
        iVar7 = (uint)(byte)*puVar18 * 0x14;
        break;
      case 0xb:
        DAT_800e1e81 = 10;
        iVar7 = (uint)(byte)*puVar18 * 0x38;
        puVar15 = &DAT_800417a0;
        break;
      case 0xc:
        puVar15 = &DAT_8004b0d4;
        iVar7 = (uint)(byte)*puVar18 * 0x2c;
        textbox_text_ptr = puVar18;
LAB_ADV_BIN__800671f4:
        DAT_800e1e81 = 10;
        puVar19 = (ushort *)(puVar15 + iVar7);
        textbox_state_flags = textbox_state_flags | 0x4001;
        goto LAB_ADV_BIN__80066cf0;
      case 0xd:
        textbox_state_flags = textbox_state_flags | 1;
        DAT_800e1e81 = 0xff;
        puVar20 = (ushort *)(&PTR_DAT_8004d410)[(byte)*puVar18];
        textbox_text_ptr = puVar18;
        goto switchD_ADV_BIN__80066e7c_default;
      case 0xe:
        DAT_800e1e81 = 0xff;
        textbox_state_flags = textbox_state_flags | 0x10001;
        iVar7 = (uint)(byte)*puVar18 * 8;
        DAT_800e1e80 = (&DAT_8004d766)[iVar7];
        puVar19 = (ushort *)(&PTR_DAT_8004d760)[(uint)(byte)*puVar18 * 2];
        textbox_text_ptr = puVar18;
        adv_textbox_animate_choice(&DAT_800e1e60,0,0,(byte)(&DAT_8004d764)[iVar7] - 1,0x16);
        adv_textbox_animate_choice(&DAT_800e1e70,0,0,(byte)(&DAT_8004d765)[iVar7] - 1,0x1a);
        bVar12 = 0;
        if (DAT_800e1e80 != 0) {
          uVar6 = 0;
          do {
            bVar12 = bVar12 + 1;
            (&DAT_ADV_BIN__800b1abc)[uVar6 * 8] = 0;
            (&DAT_ADV_BIN__800b1abd)[uVar6 * 8] = 0xb4;
            uVar6 = (uint)bVar12;
          } while (bVar12 < DAT_800e1e80);
        }
        uVar6 = (uint)DAT_800e1e80;
        uVar10 = uVar6;
        while (uVar6 < 0xf) {
          uVar10 = uVar10 + 1;
          (&DAT_ADV_BIN__800b1abc)[uVar6 * 8] = 0xff;
          (&DAT_ADV_BIN__800b1abd)[uVar6 * 8] = 0xff;
          uVar6 = uVar10 & 0xff;
        }
        goto LAB_ADV_BIN__80066c50;
      case 0xf:
        bVar12 = (byte)*puVar18;
        puVar15 = &DAT_80049040;
LAB_ADV_BIN__80067230:
        DAT_800e1e81 = 5;
        puVar19 = (ushort *)(puVar15 + (bVar12 - 1) * 0x14);
        textbox_state_flags = textbox_state_flags | 1;
        textbox_text_ptr = puVar18;
        goto LAB_ADV_BIN__80066c50;
      case 0x10:
        goto switchD_ADV_BIN__80066e7c_caseD_10;
      case 0x11:
        textbox_text_ptr = (ushort *)((int)puVar19 + 1);
        uVar17 = 0;
        uVar13 = 0;
        pcVar3 = &DAT_800e1e82;
        do {
          pcVar16 = pcVar3;
          *pcVar16 = '\0';
          uVar13 = uVar13 + 1;
          pcVar3 = pcVar16 + 1;
        } while (uVar13 < 8);
        if (uVar13 != 0) {
          uVar6 = (uint)uVar13;
          do {
            uVar11 = (&DAT_ADV_BIN__800b1804)[uVar6];
            uVar13 = uVar13 - 1;
            if (uVar11 <= uVar10) {
              if (uVar11 == 0) {
                trap(0x1c00);
              }
              *pcVar16 = (char)(uVar10 / uVar11);
              uVar6 = (&DAT_ADV_BIN__800b1804)[uVar6];
              uVar10 = uVar10 % uVar6;
              if (uVar6 == 0) {
                trap(0x1c00);
              }
            }
            uVar6 = (uint)uVar13;
            pcVar16 = pcVar16 + -1;
          } while (uVar6 != 0);
        }
        uVar13 = 0;
        do {
          pcVar16 = pcVar16 + 1;
          if (*pcVar16 != '\0') {
            uVar17 = uVar13;
          }
          uVar13 = uVar13 + 1;
        } while (uVar13 < 8);
        DAT_800e1e81 = (char)uVar17 + 1;
        bVar12 = 0;
        if (DAT_800e1e81 != 0) {
          uVar6 = 0;
          do {
            bVar12 = bVar12 + 1;
            (&DAT_800e1e82)[uVar6] = (&DAT_800e1e82)[uVar6] + -0x40;
            uVar6 = (uint)bVar12;
          } while (bVar12 < DAT_800e1e81);
        }
        goto LAB_ADV_BIN__800676a4;
      case 0x12:
        textbox_text_ptr = (ushort *)((int)puVar19 + 1);
        uVar6 = 0;
        sVar5 = FUN_ADV_BIN__8008ee6c(0x23);
        if (sVar5 != -1) {
          uVar6 = (uint)((ushort)(&DAT_801f267c)[sVar5] >> 9);
        }
        uVar17 = 0;
        uVar13 = 0;
        pcVar3 = &DAT_800e1e82;
        do {
          pcVar16 = pcVar3;
          *pcVar16 = '\0';
          uVar13 = uVar13 + 1;
          pcVar3 = pcVar16 + 1;
        } while (uVar13 < 2);
        if (uVar13 != 0) {
          uVar10 = (uint)uVar13;
          do {
            uVar11 = (&DAT_ADV_BIN__800b1804)[uVar10];
            uVar13 = uVar13 - 1;
            if (uVar11 <= uVar6) {
              if (uVar11 == 0) {
                trap(0x1c00);
              }
              *pcVar16 = (char)(uVar6 / uVar11);
              uVar10 = (&DAT_ADV_BIN__800b1804)[uVar10];
              uVar6 = uVar6 % uVar10;
              if (uVar10 == 0) {
                trap(0x1c00);
              }
            }
            uVar10 = (uint)uVar13;
            pcVar16 = pcVar16 + -1;
          } while (uVar10 != 0);
        }
        uVar13 = 0;
        do {
          pcVar16 = pcVar16 + 1;
          if (*pcVar16 != '\0') {
            uVar17 = uVar13;
          }
          uVar13 = uVar13 + 1;
        } while (uVar13 < 2);
        DAT_800e1e81 = (char)uVar17 + 1;
        bVar12 = 0;
        if (DAT_800e1e81 != 0) {
          uVar6 = 0;
          do {
            bVar12 = bVar12 + 1;
            (&DAT_800e1e82)[uVar6] = (&DAT_800e1e82)[uVar6] + -0x40;
            uVar6 = (uint)bVar12;
          } while (bVar12 < DAT_800e1e81);
        }
LAB_ADV_BIN__800676a4:
        textbox_state_flags = textbox_state_flags | 0x204001;
        puVar20 = (ushort *)(&DAT_800e1e81 + DAT_800e1e81);
        goto switchD_ADV_BIN__80066e7c_default;
      case 0x13:
        DAT_800e1e81 = 10;
        textbox_state_flags = textbox_state_flags | 0x4001;
        puVar19 = (ushort *)
                  (&DAT_ADV_BIN__800b24a4 +
                  ((byte)(&DAT_8004b0e0)[(uint)(byte)*puVar18 * 0x2c] - 1) * 10);
        textbox_text_ptr = puVar18;
        goto LAB_ADV_BIN__80066cf0;
      default:
        goto switchD_ADV_BIN__80066e7c_default;
      }
      puVar19 = (ushort *)(puVar15 + iVar7);
      textbox_state_flags = textbox_state_flags | 0x4001;
      textbox_text_ptr = puVar18;
LAB_ADV_BIN__80066cf0:
      bVar12 = (byte)*puVar19;
      if ((textbox_state_flags & 0x200000) == 0) {
        puVar18 = (ushort *)((int)puVar19 + 1);
      }
      else {
        puVar18 = (ushort *)((int)puVar19 + -1);
      }
      if ((bVar12 == 0xff) || (DAT_800e1e81 == 0)) {
        if ((textbox_state_flags & 1) == 0) {
LAB_ADV_BIN__80066f24:
          textbox_state_flags = textbox_state_flags | 0x8000;
          puVar20 = puVar18;
        }
        else {
          textbox_state_flags = textbox_state_flags & 0xfffe ^ 0x4000;
          puVar20 = (ushort *)((int)textbox_text_ptr + 1);
        }
      }
      else {
        adv_draw_jp_glyph((DAT_800e1e56 + 1 & 0xf) << 2 | 0x3c0,
                          (int)(((DAT_800e1e56 + 1 & 0xfffffff0) + 0x100) * 0x10000) >> 0x10,bVar12)
        ;
        adv_textbox_update_cursor(DAT_800e1e56,bVar12);
        DAT_800e1e56 = DAT_800e1e56 + 1;
        DAT_800e1e52 = DAT_800e1e54;
        if ((textbox_state_flags & 4) == 0) {
          if (0x1d < DAT_800e1e56) {
            textbox_state_flags = textbox_state_flags | 4;
          }
        }
        else if ((uint)DAT_800e1e56 % 0xf == 0) {
          textbox_state_flags = textbox_state_flags | 2;
        }
        DAT_800e1e81 = DAT_800e1e81 - 1;
        puVar20 = puVar18;
      }
      goto switchD_ADV_BIN__80066e7c_default;
    }
    DAT_ADV_BIN__800b8f06 = DAT_ADV_BIN__800b8f06 + 4;
    puVar20 = puVar19;
    if ((DAT_ADV_BIN__800b8f06 & 0xf) == 0) {
      iVar14 = 0;
      iVar7 = ((DAT_800e1e56 + 0xf) / 0xf & 3) * 0xf;
      iVar8 = iVar7;
      do {
        *(undefined2 *)(&DAT_ADV_BIN__800bca54 + iVar8 * 2) = 0;
        iVar14 = iVar14 + 1;
        iVar8 = iVar7 + iVar14;
      } while (iVar14 < 0xf);
      uVar6 = 0xfffffffd;
      puVar18 = puVar19;
LAB_ADV_BIN__800670b0:
      textbox_state_flags = textbox_state_flags & uVar6;
      puVar20 = puVar18;
    }
    goto switchD_ADV_BIN__80066e7c_default;
  }
  iVar7 = adv_textbox_animate_window(&DAT_800e1e60);
  if (iVar7 == 0) {
    adv_textbox_animate_window(&DAT_800e1e70);
  }
  adv_set_window_pos_size
            (0x2e,0x1e,(int)(((DAT_800e1e80 + 1) * DAT_800e1e70 * 0x10 + 0x28) * 0x10000) >> 0x10,
             (DAT_800e1e60 * 0x10 + 0xb4) * 0x10000 >> 0x10);
  cVar4 = FUN_ADV_BIN__8008f104(1);
  if (cVar4 == '\0') goto switchD_ADV_BIN__80066e7c_default;
  textbox_state_flags = textbox_state_flags ^ 0x20000;
                    /* WARNING: Read-only address (ram,0x800e1e60) is written */
                    /* WARNING: Read-only address (ram,0x800e1e70) is written */
  if (DAT_800e1e68 == 0) {
    DAT_ADV_BIN__800bc4a8 = (char)DAT_800e1e70;
    if (DAT_800e1e78 == 0) goto LAB_ADV_BIN__80066b74;
  }
  else if (DAT_800e1e78 == 0) {
LAB_ADV_BIN__80066b74:
    DAT_ADV_BIN__800bc4a8 = (char)DAT_800e1e60;
  }
  else {
    DAT_ADV_BIN__800bc4a8 = ((char)DAT_800e1e78 + '\x01') * (char)DAT_800e1e60 + (char)DAT_800e1e70;
  }
  adv_finalize_window(0x2e);
  adv_textbox_copy_state(auStack_18,&DAT_ADV_BIN__800b1a18);
  adv_textbox_clear_scroll(0);
switchD_ADV_BIN__80066e7c_default:
  if ((textbox_state_flags & 1) == 0) {
    textbox_text_ptr = puVar20;
                    /* WARNING: Read-only address (ram,0x800e1e60) is written */
                    /* WARNING: Read-only address (ram,0x800e1e68) is written */
                    /* WARNING: Read-only address (ram,0x800e1e70) is written */
                    /* WARNING: Read-only address (ram,0x800e1e78) is written */
                    /* WARNING: Read-only address (ram,0x800e1e60) is written */
                    /* WARNING: Read-only address (ram,0x800e1e68) is written */
                    /* WARNING: Read-only address (ram,0x800e1e70) is written */
                    /* WARNING: Read-only address (ram,0x800e1e78) is written */
                    /* WARNING: Read-only address (ram,0x800e1e60) is written */
                    /* WARNING: Read-only address (ram,0x800e1e68) is written */
                    /* WARNING: Read-only address (ram,0x800e1e70) is written */
                    /* WARNING: Read-only address (ram,0x800e1e78) is written */
    return 0;
  }
  DAT_800e1e5c = puVar20;
  return 0;
switchD_ADV_BIN__80066e7c_caseD_10:
  DAT_800e1e81 = 5;
  puVar19 = (ushort *)(&DAT_80049040 + ((byte)*puVar18 - 1) * 0x14);
  textbox_state_flags = textbox_state_flags | 0x40001;
  textbox_text_ptr = puVar18;
  goto LAB_ADV_BIN__80066c50;
}

