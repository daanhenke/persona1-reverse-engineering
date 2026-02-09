
/* WARNING: Globals starting with '_' overlap smaller symbols at the same address */

int adv_execute_event_script(int script_ptr)

{
  undefined1 *puVar1;
  byte bVar2;
  byte bVar3;
  undefined1 uVar4;
  undefined1 uVar5;
  bool bVar6;
  short sVar7;
  short sVar8;
  short sVar9;
  byte bVar10;
  undefined1 uVar11;
  char cVar12;
  short sVar13;
  undefined4 uVar14;
  uint uVar15;
  uint uVar16;
  int iVar17;
  byte *pbVar18;
  char *pcVar19;
  undefined4 uVar20;
  int iVar21;
  uint uVar22;
  int return_code;
  undefined1 auStack_68 [4];
  undefined1 auStack_64 [4];
  undefined1 *local_60;
  
  puVar1 = auStack_68 + 3;
  uVar16 = (uint)puVar1 & 3;
  *(uint *)(puVar1 + -uVar16) =
       *(uint *)(puVar1 + -uVar16) & -1 << (uVar16 + 1) * 8 |
       DAT_ADV_BIN__80065500 >> (3 - uVar16) * 8;
  auStack_68 = (undefined1  [4])DAT_ADV_BIN__80065500;
  puVar1 = auStack_64 + 3;
  uVar16 = (uint)puVar1 & 3;
  *(uint *)(puVar1 + -uVar16) =
       *(uint *)(puVar1 + -uVar16) & -1 << (uVar16 + 1) * 8 |
       DAT_ADV_BIN__80065504 >> (3 - uVar16) * 8;
  auStack_64 = (undefined1  [4])DAT_ADV_BIN__80065504;
  return_code = 0;
  local_60 = &DAT_801f2ac4;
  iVar17 = script_resume_ptr;
  if (script_ptr != -1) {
    adv_finalize_window(0x34);
    s_V_P_FT4_ADV_BIN__800bc478[0] = '\x10';
    s_V_P_FT4_ADV_BIN__800bc478[1] = '\0';
LAB_ADV_BIN__800ac260:
    do {
      uVar20 = DAT_801f2678;
      sVar8 = DAT_ADV_BIN__800bc704;
      sVar13 = DAT_ADV_BIN__800bc6f8;
      iVar17 = script_resume_ptr;
      DAT_801f2678 = uVar20;
      switch(*(undefined1 *)(script_ptr + 1)) {
      case 0x21:
        goto switchD_ADV_BIN__800ac290_caseD_21;
      case 0x22:
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x23:
        uVar16 = rand();
        if ((uint)*(byte *)(script_ptr + 2) < (uVar16 & 0xff)) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x24:
        adv_set_event_flag(*(undefined2 *)(script_ptr + 2));
        break;
      case 0x25:
        adv_clear_event_flag(*(undefined2 *)(script_ptr + 2));
        break;
      case 0x26:
        iVar17 = adv_check_event_flag(*(undefined2 *)(script_ptr + 2));
        if (iVar17 == 0) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x27:
        FUN_ADV_BIN__800addb0(*(undefined1 *)(script_ptr + 2));
        if (0xcf < *(byte *)(script_ptr + 2)) {
          encounter_resume_flag = 1;
          return_code = 5;
        }
        break;
      case 0x28:
        next_event_id = (ushort)*(byte *)(script_ptr + 2);
        return_code = 2;
        break;
      case 0x29:
        _current_event_id = *(ushort *)(script_ptr + 2);
        current_map_x = *(undefined1 *)(script_ptr + 4);
        current_map_y = *(undefined1 *)(script_ptr + 5);
        current_overlay_type = *(undefined1 *)(script_ptr + 6);
        return_code = 3;
        break;
      case 0x2a:
        DAT_801f1bc8 = 1;
        uVar11 = *(undefined1 *)(script_ptr + 2);
        FUN_ADV_BIN__80085db8();
        FUN_ADV_BIN__80099304(uVar11);
        FUN_ADV_BIN__80085ec0();
        if (DAT_801f1bca == 0) {
          adv_reload_tilemap_gfx();
          uVar20 = 4;
          goto LAB_ADV_BIN__800acec8;
        }
        FUN_ADV_BIN__800891ec();
        break;
      case 0x2b:
        next_event_id = *(ushort *)(script_ptr + 2);
        current_overlay_type = *(undefined1 *)(script_ptr + 4);
        return_code = 1;
        break;
      case 0x2c:
        _current_event_id = (ushort)*(byte *)(script_ptr + 2);
        current_event_param = *(undefined1 *)(script_ptr + 3);
        current_map_x = *(undefined1 *)(script_ptr + 4);
        current_map_y = *(undefined1 *)(script_ptr + 5);
        current_overlay_type = *(undefined1 *)(script_ptr + 6);
        return_code = 4;
        break;
      case 0x2d:
        movie_or_ending_id = (ushort)*(byte *)(script_ptr + 2);
        return_code = 6;
        break;
      case 0x2e:
        if (DAT_801f2b34 != *(char *)(script_ptr + 2)) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x2f:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        bVar6 = (byte)(&DAT_801f1c17)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] <
                *(byte *)(script_ptr + 3);
        goto LAB_ADV_BIN__800ac4e8;
      case 0x30:
        iVar17 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        iVar17 = iVar17 << 0x10;
        goto LAB_ADV_BIN__800ac508;
      case 0x31:
        iVar21 = 0;
        uVar16 = FUN_ADV_BIN__800b04dc();
        uVar16 = uVar16 & 0xff;
        FUN_ADV_BIN__800ae628(uVar16);
        bVar6 = false;
        iVar17 = 0;
        FUN_ADV_BIN__800b0578(uVar16,*(undefined1 *)(script_ptr + 2),DAT_801f1c17);
        FUN_ADV_BIN__800ae698();
        pcVar19 = &DAT_801f1deb;
        do {
          if ((pcVar19[-0x27] != '\0') && (*pcVar19 == *(char *)(script_ptr + 2))) {
            (&DAT_801f1c24)[uVar16 * 0x60 + iVar17] = (char)iVar21;
            iVar17 = iVar17 + 1;
            bVar6 = true;
          }
          iVar21 = iVar21 + 1;
          pcVar19 = pcVar19 + 0x40;
        } while (iVar21 < 0x1f);
        if (bVar6) {
          (&DAT_801f1c23)[uVar16 * 0x60] = 0;
          FUN_ADV_BIN__800b0ae0(1,DAT_801f1c17,uVar16,*(undefined1 *)(script_ptr + 2));
        }
        (&DAT_801f1c23)[uVar16 * 0x60] = 0;
        uVar14 = FUN_ADV_BIN__8007dbe8((&DAT_801f1c22)[uVar16 * 0x60] + -1,0,0);
        (&DAT_801f1be8)[uVar16 * 0x18] = uVar14;
        FUN_ADV_BIN__80090654(uVar16);
        goto LAB_ADV_BIN__800acfb8;
      case 0x32:
        uVar11 = FUN_ADV_BIN__800b047c(*(undefined1 *)(script_ptr + 2));
        uVar16 = FUN_ADV_BIN__800ae720(uVar11);
        uVar22 = (uint)(byte)(&DAT_801f256c)[uVar16 & 0xff];
        FUN_ADV_BIN__8008f058(&DAT_801f267c,&DAT_800eae4c,0x17f);
        FUN_ADV_BIN__8008d4e4(uVar22,0);
        FUN_ADV_BIN__8008d4e4(uVar22,1);
        FUN_ADV_BIN__8008d4e4(uVar22,2);
        FUN_ADV_BIN__8008d4e4(uVar22,3);
        FUN_ADV_BIN__8008d4e4(uVar22,4);
        FUN_ADV_BIN__8008d4e4(uVar22,5);
        FUN_ADV_BIN__8008d4e4(uVar22,6);
        FUN_ADV_BIN__8008ef2c();
        FUN_ADV_BIN__8008f0b4();
        (&DAT_801f256c)[uVar16 & 0xff] = 0xff;
        iVar17 = uVar22 * 0x60;
        (&DAT_801f1c0a)[iVar17] = 0;
        (&DAT_801f1c2b)[iVar17] = (&DAT_801f1c22)[iVar17];
        goto LAB_ADV_BIN__800ad054;
      case 0x33:
        FUN_ADV_BIN__800b02f0(*(undefined1 *)(script_ptr + 2));
        break;
      case 0x34:
        cVar12 = FUN_ADV_BIN__800b02a8(*(undefined1 *)(script_ptr + 2));
        if (cVar12 == -1) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x35:
        FUN_ADV_BIN__800b0328(*(undefined1 *)(script_ptr + 2));
        break;
      case 0x36:
        iVar17 = FUN_ADV_BIN__800b0f74();
        iVar17 = iVar17 << 0x10;
        goto LAB_ADV_BIN__800ac508;
      case 0x37:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        bVar6 = (byte)(&DAT_801f1c22)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] <
                *(byte *)(script_ptr + 3);
LAB_ADV_BIN__800ac4e8:
        if (!bVar6) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x38:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        bVar6 = (uint)(&DAT_801f1be8)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x18] <
                *(uint *)(script_ptr + 4);
        goto LAB_ADV_BIN__800acdcc;
      case 0x39:
        sVar13 = FUN_ADV_BIN__800b0ed0(*(undefined1 *)(script_ptr + 2));
        uVar22 = (uint)sVar13;
        uVar16 = 0;
        if (uVar22 != 0xffffffff) {
          iVar17 = 0;
          do {
            uVar15 = FUN_ADV_BIN__800b0f18(uVar16 & 0xff,uVar22 & 0xff);
            uVar15 = uVar15 & 0xff;
            if (uVar15 != 0xff) {
              (&DAT_801f1c24)[iVar17 + uVar15] = 0xff;
              if ((byte)(&DAT_801f1c23)[iVar17] == uVar15) {
                (&DAT_801f1c23)[iVar17] = 0xff;
              }
              uVar11 = FUN_ADV_BIN__800ae720(uVar16 & 0xff);
              FUN_ADV_BIN__800903a0(uVar11);
            }
            uVar16 = uVar16 + 1;
            iVar17 = iVar17 + 0x60;
          } while ((int)uVar16 < 5);
          pbVar18 = &DAT_801f2574;
          do {
            if (*pbVar18 == uVar22) {
              *pbVar18 = 0xff;
            }
            pbVar18 = pbVar18 + 1;
          } while ((int)pbVar18 < -0x7fe0da7c);
          (&DAT_801f1dc4)[uVar22 * 0x40] = 0;
        }
        break;
      case 0x3a:
        iVar17 = FUN_ADV_BIN__8008ee6c(*(undefined1 *)(script_ptr + 2));
        iVar17 = iVar17 << 0x10;
        goto LAB_ADV_BIN__800ac508;
      case 0x3b:
        sVar13 = FUN_ADV_BIN__8008ee6c(*(undefined1 *)(script_ptr + 2));
        if (sVar13 != 99) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x3c:
        FUN_ADV_BIN__800b13dc((int)*(short *)(script_ptr + 2),*(undefined1 *)(script_ptr + 4));
        DAT_801f2678 = uVar20;
        break;
      case 0x3d:
        FUN_ADV_BIN__800b14c8((int)*(short *)(script_ptr + 2),*(undefined1 *)(script_ptr + 4));
        DAT_801f2678 = uVar20;
        break;
      case 0x3e:
        bVar6 = player_money < *(uint *)(script_ptr + 4);
        goto LAB_ADV_BIN__800acdcc;
      case 0x3f:
        if (*(char *)(script_ptr + 2) == '\0') {
          iVar17 = *(int *)(script_ptr + 4);
        }
        else {
          iVar17 = -*(int *)(script_ptr + 4);
        }
        player_money = player_money + iVar17;
        if (999999999 < (int)player_money) {
          player_money = 999999999;
        }
        if ((int)player_money < 0) {
          player_money = 0;
        }
        break;
      case 0x40:
        if (*(char *)(script_ptr + 2) != protagonist_level) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x41:
        DAT_801f2b32 = *(undefined1 *)(script_ptr + 3);
        break;
      case 0x42:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        iVar17 = (int)sVar13;
        if (iVar17 != -1) {
          (&DAT_801f1bcc)[(uint)*(byte *)(script_ptr + iVar17) * 0x18] =
               (&DAT_801f1bcc)[(uint)*(byte *)(script_ptr + iVar17) * 0x18] -
               (int)((uint)*(byte *)(script_ptr + 2) *
                    (&DAT_801f1bcc)[(uint)(byte)(&DAT_801f256c)[iVar17] * 0x18]) / 0xff;
        }
        break;
      case 0x43:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        iVar17 = (int)sVar13;
        if (iVar17 != -1) {
          (&DAT_801f1bd4)[(uint)*(byte *)(script_ptr + iVar17) * 0x18] =
               (&DAT_801f1bd4)[(uint)*(byte *)(script_ptr + iVar17) * 0x18] -
               (int)((uint)*(byte *)(script_ptr + 2) *
                    (&DAT_801f1bd4)[(uint)(byte)(&DAT_801f256c)[iVar17] * 0x18]) / 0xff;
        }
        break;
      case 0x44:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        if (sVar13 != -1) {
          if ((&DAT_801f1bcc)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x18] ==
              (&DAT_801f1bd0)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x18])
          goto switchD_ADV_BIN__800ac290_caseD_22;
          (&DAT_801f1bcc)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x18] =
               (&DAT_801f1bd0)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x18];
        }
        break;
      case 0x45:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        if (sVar13 != -1) {
          uVar16 = (uint)(byte)(&DAT_801f256c)[sVar13];
          if ((&DAT_801f1bd4)[uVar16 * 0x18] == (&DAT_801f1bd8)[uVar16 * 0x18])
          goto switchD_ADV_BIN__800ac290_caseD_22;
          (&DAT_801f1bd4)[uVar16 * 0x18] = (&DAT_801f1bd8)[uVar16 * 0x18];
        }
        break;
      case 0x46:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        if ((sVar13 == -1) ||
           ((&DAT_801f1c15)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] == *(char *)(script_ptr + 2)
           )) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x47:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        if ((&DAT_801f1c15)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] != *(char *)(script_ptr + 3)
           ) {
          (&DAT_801f1c15)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] =
               *(undefined1 *)(script_ptr + 3);
          break;
        }
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x48:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        if (sVar13 != -1) {
          if ((&DAT_801f1c15)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] !=
              *(char *)(script_ptr + 3)) goto switchD_ADV_BIN__800ac290_caseD_22;
          (&DAT_801f1c15)[(uint)(byte)(&DAT_801f256c)[sVar13] * 0x60] = 0;
        }
        break;
      case 0x49:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        bVar10 = FUN_ADV_BIN__800b11e4((&DAT_801f256c)[sVar13],*(undefined1 *)(script_ptr + 4));
        bVar6 = bVar10 < *(byte *)(script_ptr + 4);
LAB_ADV_BIN__800acdcc:
        if (bVar6) {
          script_ptr = *(int *)(script_ptr + 8);
          goto LAB_ADV_BIN__800ac260;
        }
        break;
      case 0x4a:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        FUN_ADV_BIN__800b126c
                  ((&DAT_801f256c)[sVar13],*(undefined1 *)(script_ptr + 3),
                   *(undefined1 *)(script_ptr + 5),*(undefined1 *)(script_ptr + 4));
        break;
      case 0x4b:
        FUN_ADV_BIN__80085db8();
        iVar17 = FUN_ADV_BIN__80099304(0x24);
        FUN_ADV_BIN__80085ec0();
        adv_reload_tilemap_gfx();
        adv_fade_transition(4,0x80);
        if (iVar17 != 0) {
          return_code = 7;
        }
        break;
      case 0x4c:
        FUN_ADV_BIN__80085db8();
        FUN_ADV_BIN__80085ec0();
        FUN_ADV_BIN__8007183c();
        FUN_ADV_BIN__80091cd0(1);
        adv_reload_tilemap_gfx();
        FUN_ADV_BIN__80068750((int)&DAT_80118000 + DAT_80118004,0x380,0x1c8,0x100,0x1f8);
        FUN_ADV_BIN__80068750((int)&DAT_80118000 + DAT_80118000,0x380,0x100,0x3c0,0x1a0);
        uVar20 = 8;
LAB_ADV_BIN__800acec8:
        adv_fade_transition(uVar20,0x80);
        break;
      case 0x4d:
        iVar17 = 0;
        if (*(short *)(script_ptr + 2) != 0) {
          do {
            iVar17 = iVar17 + 1;
            adv_vsync_and_render();
          } while (iVar17 < (int)(uint)*(ushort *)(script_ptr + 2));
        }
        break;
      case 0x4e:
        cVar12 = FUN_ADV_BIN__800b03bc();
        goto LAB_ADV_BIN__800acf18;
      case 0x4f:
        sVar13 = FUN_ADV_BIN__800b0f74();
        FUN_ADV_BIN__800b1014((int)sVar13 & 0xff,*(undefined1 *)(script_ptr + 3));
        uVar16 = FUN_ADV_BIN__800b047c(*(undefined1 *)(script_ptr + 2));
        uVar16 = uVar16 & 0xff;
        bVar10 = FUN_ADV_BIN__800b0fb8(uVar16);
        iVar17 = uVar16 * 0x60;
        (&DAT_801f1c24)[iVar17 + (uint)bVar10] = (char)sVar13;
        (&DAT_801f1c23)[iVar17] = bVar10;
        (&DAT_801f1deb)[sVar13 * 0x40] = (&DAT_801f1c0a)[iVar17];
LAB_ADV_BIN__800acfb8:
        FUN_ADV_BIN__800903a0(uVar16);
        DAT_801f2678 = uVar20;
        break;
      case 0x50:
        iVar17 = FUN_ADV_BIN__800b0ed0(*(undefined1 *)(script_ptr + 2));
        iVar17 = iVar17 << 0x10;
LAB_ADV_BIN__800ac508:
        if (iVar17 >> 0x10 != -1) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x51:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        cVar12 = FUN_ADV_BIN__800b0fb8((&DAT_801f256c)[sVar13]);
LAB_ADV_BIN__800acf18:
        if (cVar12 != -1) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x52:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        (&DAT_801f256c)[sVar13] = 0xff;
        goto LAB_ADV_BIN__800ad054;
      case 0x53:
        uVar11 = FUN_ADV_BIN__800b0528(*(undefined1 *)(script_ptr + 2));
        FUN_ADV_BIN__800ae628(uVar11);
LAB_ADV_BIN__800ad054:
        FUN_ADV_BIN__800ae698();
        DAT_801f2678 = uVar20;
        break;
      case 0x54:
        if (*(char *)(script_ptr + 2) != DAT_ADV_BIN__800bc4a8) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x55:
        adv_setup_dialogue_box
                  (*(undefined4 *)(script_ptr + 4),(&DAT_ADV_BIN__800b1ab0)[(byte)local_60[8]]);
        script_ptr = script_ptr + (uint)(byte)(&DAT_ADV_BIN__800bb78c)[*(byte *)(script_ptr + 1)];
        adv_init_text_layer(0x18,0,0);
        adv_init_text_layer(0x19,0,0);
        adv_init_text_layer(0x1a,0,0);
        adv_init_text_layer(0x1b,0,0);
        while (iVar17 = 0, (textbox_state_flags & 0x8000) == 0) {
          adv_textbox_process();
          adv_vsync_and_render();
        }
        do {
          iVar17 = iVar17 + 1;
          adv_vsync_and_render();
        } while (iVar17 < 0x18);
        SsSetNck(DAT_801f53ac);
        SsSetNck(DAT_801f53ae);
        SsSetNck(DAT_801f53b0);
        SsSetNck(DAT_801f53b2);
        goto LAB_ADV_BIN__800ac260;
      case 0x56:
        FUN_ADV_BIN__800b1548(*(undefined1 *)(script_ptr + 2));
        break;
      case 0x57:
        sVar13 = FUN_ADV_BIN__800b0400(*(undefined1 *)(script_ptr + 2));
        uVar16 = (uint)(byte)(&DAT_801f256c)[sVar13];
        (&DAT_801f1c2a)[uVar16 * 0x60] = *(undefined1 *)(script_ptr + 3);
        FUN_ADV_BIN__80090654(uVar16);
        FUN_ADV_BIN__800903a0(uVar16);
        break;
      case 0x58:
        (&DAT_801f15d8)[(uint)*(byte *)(script_ptr + 2) * 0xb] = *(undefined4 *)(script_ptr + 4);
        break;
      case 0x59:
        sVar13 = FUN_ADV_BIN__800b1578();
        iVar17 = (int)sVar13;
        goto LAB_ADV_BIN__800ad184;
      case 0x5a:
        iVar17 = FUN_ADV_BIN__80076ec0();
LAB_ADV_BIN__800ad184:
        if ((uint)*(byte *)(script_ptr + 2) != iVar17 + 1U) break;
        goto switchD_ADV_BIN__800ac290_caseD_22;
      case 0x60:
        adv_clear_text_layer(0);
        adv_clear_text_layer(1);
        adv_clear_text_layer(2);
        adv_clear_text_layer(3);
        DAT_ADV_BIN__800b8f06 = 0;
        DAT_800e1e56 = 0;
        adv_textbox_copy_state(auStack_68,&DAT_ADV_BIN__800b1a18);
        FUN_ADV_BIN__800af940(0);
        break;
      case 0x61:
        FUN_ADV_BIN__800afc7c(0);
        break;
      case 99:
        current_background_id = *(undefined1 *)(script_ptr + 2);
        FUN_ADV_BIN__80086b3c();
        break;
      case 100:
        uVar16 = (uint)*(byte *)(script_ptr + 2);
        iVar17 = uVar16 * 0x2c;
        (&DAT_801f15fa)[iVar17] = *(undefined1 *)(script_ptr + 3);
        (&DAT_801f1601)[iVar17] = *(byte *)(script_ptr + 8) >> 4;
        uVar11 = *(undefined1 *)(script_ptr + 4);
        (&DAT_801f15f8)[iVar17] = uVar11;
        (&DAT_801f15f4)[iVar17] = uVar11;
        uVar11 = *(undefined1 *)(script_ptr + 5);
        (&DAT_801f15f9)[iVar17] = uVar11;
        (&DAT_801f15f5)[iVar17] = uVar11;
        uVar11 = *(undefined1 *)(script_ptr + 6);
        (&DAT_801f15f0)[iVar17] = uVar11;
        (&DAT_801f15ef)[iVar17] = uVar11;
        bVar10 = *(byte *)(script_ptr + 7);
        bVar2 = *(byte *)(script_ptr + 8);
        bVar3 = *(byte *)(script_ptr + 9);
        (&DAT_801f15f1)[iVar17] = 0;
        (&DAT_801f15fd)[iVar17] = 0;
        (&DAT_801f15dc)[uVar16 * 0xb] =
             (bVar10 & 0xf) * 0x100 + (bVar2 & 0xf) * 0x80 + (uint)bVar3 * 0x200;
        (&DAT_801f15fe)[iVar17] = *(undefined1 *)(script_ptr + 0xb);
        uVar11 = *(undefined1 *)(script_ptr + 10);
        (&DAT_801f15e0)[uVar16 * 0xb] = 0xffffffff;
        (&DAT_801f15d8)[uVar16 * 0xb] = 0xffffffff;
        (&DAT_801f15f3)[iVar17] = uVar11;
        FUN_ADV_BIN__800ae764(uVar16);
        break;
      case 0x65:
        uVar22 = (uint)*(byte *)(script_ptr + 2);
        iVar17 = uVar22 * 0x2c;
        (&DAT_801f15fa)[iVar17] = *(undefined1 *)(script_ptr + 3);
        (&DAT_801f15f4)[iVar17] = *(undefined1 *)(script_ptr + 4);
        uVar11 = (&DAT_801f15f4)[iVar17];
        (&DAT_801f15f5)[iVar17] = *(undefined1 *)(script_ptr + 5);
        uVar4 = (&DAT_801f15f5)[iVar17];
        (&DAT_801f15dc)[uVar22 * 0xb] =
             (uint)*(byte *)(script_ptr + 6) * 0x80 + (uint)*(byte *)(script_ptr + 7) * 0x200;
        (&DAT_801f15fb)[iVar17] = *(undefined1 *)(script_ptr + 6);
        (&DAT_801f15f3)[iVar17] = *(undefined1 *)(script_ptr + 8);
        uVar5 = *(undefined1 *)(script_ptr + 9);
        (&DAT_801f15f0)[iVar17] = 0;
        (&DAT_801f15ef)[iVar17] = 0;
        (&DAT_801f15f1)[iVar17] = 0;
        (&DAT_801f15fd)[iVar17] = 0;
        (&DAT_801f15e0)[uVar22 * 0xb] = 0xffffffff;
        (&DAT_801f15fe)[iVar17] = uVar5;
        FUN_ADV_BIN__800836d8(uVar11,uVar4,&DAT_801f15d8 + uVar22 * 0xb);
        uVar16 = (uint)(byte)(&DAT_801f15fa)[iVar17];
        if (0x7f < uVar16) {
          uVar16 = uVar16 - 0x80;
        }
        if (((&DAT_801f15dc)[uVar22 * 0xb] & 0x80) == 0) {
          adv_setup_sprite_obj
                    (*(undefined4 *)(&DAT_80100070 + uVar16 * 4),uVar22,
                     (int)(short)(&DAT_801f15ea)[uVar22 * 0x16],
                     (int)(short)(&DAT_801f15e6)[uVar22 * 0x16],
                     (int)(short)(&DAT_801f15e8)[uVar22 * 0x16]);
        }
        else {
          FUN_ADV_BIN__80065d88
                    (*(undefined4 *)(&DAT_80100070 + uVar16 * 4),uVar22,
                     (int)(short)(&DAT_801f15ea)[uVar22 * 0x16],
                     (int)(short)(&DAT_801f15e6)[uVar22 * 0x16],
                     (int)(short)(&DAT_801f15e8)[uVar22 * 0x16]);
        }
        FUN_ADV_BIN__8006617c
                  (uVar22,(uint)(byte)(&DAT_801f15f3)[uVar22 * 0x2c] -
                          (uint)((byte)(&DAT_801f15f3)[uVar22 * 0x2c] >> 4) * 8 *
                          DAT_ADV_BIN__800bc484 & 0xff);
        (&DAT_801f15e4)[uVar22 * 0x16] = 0;
        break;
      case 0x66:
        (&DAT_801f15e4)[(uint)*(byte *)(script_ptr + 2) * 0x16] = 0xffff;
        (&DAT_801f15fa)[(uint)*(byte *)(script_ptr + 2) * 0x2c] = 0xff;
        break;
      case 0x67:
        adv_vsync_and_render();
        adv_load_resource_archive(3,*(undefined1 *)(script_ptr + 2));
        cd_read_to_address(&DAT_8005e678,5,&DAT_800f4000);
        while (DAT_80055c34 != -1) {
                    /* WARNING: Read-only address (ram,0x80118000) is written */
                    /* WARNING: Read-only address (ram,0x80118004) is written */
                    /* WARNING: Read-only address (ram,0x801f1c17) is written */
                    /* WARNING: Read-only address (ram,0x801f2b34) is written */
                    /* WARNING: Read-only address (ram,0x801f53ae) is written */
                    /* WARNING: Read-only address (ram,0x801f53b0) is written */
                    /* WARNING: Read-only address (ram,0x801f53b2) is written */
          adv_vsync_and_render();
        }
                    /* WARNING: Read-only address (ram,0x80118000) is written */
                    /* WARNING: Read-only address (ram,0x80118004) is written */
                    /* WARNING: Read-only address (ram,0x801f1c17) is written */
                    /* WARNING: Read-only address (ram,0x801f2b34) is written */
                    /* WARNING: Read-only address (ram,0x801f53ae) is written */
                    /* WARNING: Read-only address (ram,0x801f53b0) is written */
                    /* WARNING: Read-only address (ram,0x801f53b2) is written */
        FUN_ADV_BIN__80068750(&DAT_800f4008,0x140,0x168,0,0x1e6);
        adv_vsync_and_render();
        FUN_ADV_BIN__800afefc(*(undefined1 *)(script_ptr + 3));
        break;
      case 0x68:
        FUN_ADV_BIN__800b0010();
        break;
      case 0x69:
        adv_play_sfx(*(byte *)(script_ptr + 3) + 1);
        uVar16 = (uint)*(byte *)(script_ptr + 2);
        FUN_ADV_BIN__80065d88
                  (*(undefined4 *)(&DAT_ADV_BIN__800bb824 + (uint)*(byte *)(script_ptr + 3) * 4),
                   uVar16 + 0x20 & 0xff,(short)(&DAT_801f15ea)[uVar16 * 0x16] + -1,
                   (int)(short)(&DAT_801f15e6)[uVar16 * 0x16],
                   (int)(short)(&DAT_801f15e8)[uVar16 * 0x16]);
        break;
      case 0x6c:
        FUN_ADV_BIN__800aeab4(*(undefined1 *)(script_ptr + 2));
        break;
      case 0x6d:
        FUN_ADV_BIN__800aebec();
        break;
      case 0x6e:
        FUN_ADV_BIN__800aed78
                  (*(undefined1 *)(script_ptr + 2),*(undefined1 *)(script_ptr + 3),
                   *(undefined1 *)(script_ptr + 4),*(undefined1 *)(script_ptr + 5),
                   *(undefined1 *)(script_ptr + 6));
        break;
      case 0x71:
        uVar16 = (uint)*(byte *)(script_ptr + 3);
        adv_textbox_setup_scroll
                  (*(undefined1 *)(script_ptr + 2),(&DAT_80100c40)[uVar16 * 4],
                   (int)(short)(&DAT_80100c44)[uVar16 * 8],(int)(short)(&DAT_80100c46)[uVar16 * 8],
                   (int)(short)(&DAT_80100c48)[uVar16 * 8],(int)(short)(&DAT_80100c4a)[uVar16 * 8]);
        break;
      case 0x72:
        adv_textbox_clear_scroll(*(undefined1 *)(script_ptr + 2));
        break;
      case 0x73:
        (&DAT_801f15dc)[(uint)*(byte *)(script_ptr + 2) * 0xb] =
             (&DAT_801f15dc)[(uint)*(byte *)(script_ptr + 2) * 0xb] | 0x200;
        break;
      case 0x74:
        (&DAT_801f15dc)[(uint)*(byte *)(script_ptr + 2) * 0xb] =
             (&DAT_801f15dc)[(uint)*(byte *)(script_ptr + 2) * 0xb] & 0xfffffdff;
        break;
      case 0x75:
      case 0x76:
        FUN_ADV_BIN__800660dc(*(undefined1 *)(script_ptr + 2),*(undefined1 *)(script_ptr + 3));
        (&DAT_801f15f3)[(uint)*(byte *)(script_ptr + 2) * 0x2c] = 0x80;
        break;
      case 0x77:
        FUN_ADV_BIN__8006612c(*(undefined1 *)(script_ptr + 2),*(undefined1 *)(script_ptr + 3));
        (&DAT_801f15f3)[(uint)*(byte *)(script_ptr + 2) * 0x2c] = 0;
        break;
      case 0x78:
        current_npc_slot = *(undefined1 *)(script_ptr + 2);
        FUN_ADV_BIN__800841bc(current_npc_slot);
        sVar9 = DAT_ADV_BIN__800bc704;
        sVar7 = DAT_ADV_BIN__800bc6f8;
        DAT_ADV_BIN__800bc6f8 = sVar13;
        DAT_ADV_BIN__800bc704 = sVar8;
        while ((sVar9 != DAT_ADV_BIN__800bc704 || (sVar7 != DAT_ADV_BIN__800bc6f8))) {
          if (sVar9 < DAT_ADV_BIN__800bc704) {
            DAT_ADV_BIN__800bc704 = DAT_ADV_BIN__800bc704 + -1;
          }
          if (DAT_ADV_BIN__800bc704 < sVar9) {
            DAT_ADV_BIN__800bc704 = DAT_ADV_BIN__800bc704 + 1;
          }
          if (sVar7 < DAT_ADV_BIN__800bc6f8) {
            DAT_ADV_BIN__800bc6f8 = DAT_ADV_BIN__800bc6f8 + -1;
          }
          if (DAT_ADV_BIN__800bc6f8 < sVar7) {
            DAT_ADV_BIN__800bc6f8 = DAT_ADV_BIN__800bc6f8 + 1;
          }
          adv_vsync_and_render();
        }
        break;
      case 0x79:
        if (*(char *)(script_ptr + 7) == '\0') {
          FUN_ADV_BIN__800af894
                    (*(undefined1 *)(script_ptr + 2),*(undefined1 *)(script_ptr + 3),
                     *(undefined1 *)(script_ptr + 6));
          FUN_ADV_BIN__800af894
                    (*(char *)(script_ptr + 4) + '\x02',*(undefined1 *)(script_ptr + 5),
                     *(undefined1 *)(script_ptr + 6));
        }
        else {
          FUN_ADV_BIN__800af894
                    (*(char *)(script_ptr + 4) + '\x02',*(undefined1 *)(script_ptr + 5),
                     *(undefined1 *)(script_ptr + 6));
          FUN_ADV_BIN__800af894
                    (*(undefined1 *)(script_ptr + 2),*(undefined1 *)(script_ptr + 3),
                     *(undefined1 *)(script_ptr + 6));
        }
        break;
      case 0x7a:
        adv_finalize_window(*(char *)(script_ptr + 2) + ' ');
        break;
      case 0x7b:
        while (cVar12 = FUN_ADV_BIN__800aee40(current_npc_slot), cVar12 != '\0') {
          adv_vsync_and_render();
        }
        SsSeqStop(DAT_801f5390);
        break;
      case 0x7c:
        bVar10 = *(byte *)(script_ptr + 2);
        iVar17 = (uint)bVar10 * 0x2c;
        (&DAT_801f15f4)[iVar17] = *(undefined1 *)(script_ptr + 3);
        (&DAT_801f15f5)[iVar17] = *(undefined1 *)(script_ptr + 4);
        uVar11 = *(undefined1 *)(script_ptr + 5);
        (&DAT_801f15f1)[iVar17] = 0;
        (&DAT_801f15fd)[iVar17] = 0;
        (&DAT_801f15f0)[iVar17] = uVar11;
        (&DAT_801f15ef)[iVar17] = uVar11;
        (&DAT_801f15fe)[iVar17] = *(undefined1 *)(script_ptr + 6);
        FUN_ADV_BIN__800ae764((uint)bVar10);
        break;
      case 0x80:
        adv_play_bgm(*(undefined1 *)(script_ptr + 2));
        if (*(byte *)(script_ptr + 2) < 0x40) {
          FUN_80011b88(s__ADV_ADVCMD_BIN_1_ADV_BIN__80065508,&DAT_80118000);
          while (DAT_80055c34 != -1) {
            adv_vsync_and_render();
          }
        }
        break;
      case 0x81:
        adv_play_sfx(*(undefined1 *)(script_ptr + 2));
        break;
      case 0x87:
        if ((calendar_month <= *(byte *)(script_ptr + 2)) &&
           ((*(byte *)(script_ptr + 2) != calendar_month ||
            (calendar_day <= *(byte *)(script_ptr + 3))))) break;
switchD_ADV_BIN__800ac290_caseD_22:
        script_ptr = *(int *)(script_ptr + 4);
        goto LAB_ADV_BIN__800ac260;
      case 0x88:
        calendar_enabled = 0;
        break;
      case 0x89:
        calendar_enabled = 1;
        break;
      case 0x8a:
        DAT_801f29c3 = 0;
        DAT_801f29c2 = 0;
        calendar_day = 0;
        calendar_month = 0;
      }
      script_ptr = script_ptr + (uint)(byte)(&DAT_ADV_BIN__800bb78c)[*(byte *)(script_ptr + 1)];
      iVar17 = script_ptr;
    } while (return_code == 0);
  }
switchD_ADV_BIN__800ac290_caseD_21:
  script_resume_ptr = iVar17;
  current_npc_slot = 0;
  return return_code;
}

