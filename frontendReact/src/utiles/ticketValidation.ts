import type { TicketPriority } from "../types/ticket";

const ticketPriorities: TicketPriority[] = ["low", "normal", "high"];

export function validateTicketTitle(value: string): string | null {
  const title = value.trim();

  if (!title) {
    return "РќР°Р·РІР°РЅРёРµ Р·Р°СЏРІРєРё РѕР±СЏР·Р°С‚РµР»СЊРЅРѕ";
  }

  if (title.length < 3) {
    return "РќР°Р·РІР°РЅРёРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РЅРµ РєРѕСЂРѕС‡Рµ 3 СЃРёРјРІРѕР»РѕРІ";
  }

  if (title.length > 120) {
    return "РќР°Р·РІР°РЅРёРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РЅРµ РґР»РёРЅРЅРµРµ 120 СЃРёРјРІРѕР»РѕРІ";
  }

  return null;
}

export function validateTicketDescription(value: string): string | null {
  const description = value.trim();

  if (description.length > 1000) {
    return "РћРїРёСЃР°РЅРёРµ РґРѕР»Р¶РЅРѕ Р±С‹С‚СЊ РЅРµ РґР»РёРЅРЅРµРµ 1000 СЃРёРјРІРѕР»РѕРІ";
  }

  return null;
}

export function validateTicketPriority(value: string): string | null {
  const priority = value.trim();

  if (!ticketPriorities.includes(priority as TicketPriority)) {
    return "Р’С‹Р±РµСЂРёС‚Рµ РєРѕСЂСЂРµРєС‚РЅС‹Р№ РїСЂРёРѕСЂРёС‚РµС‚";
  }

  return null;
}
