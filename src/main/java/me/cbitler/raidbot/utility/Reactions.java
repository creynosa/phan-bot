package me.cbitler.raidbot.utility;

import me.cbitler.raidbot.RaidBot;
import net.dv8tion.jda.core.entities.Emote;

import java.util.ArrayList;
import java.util.Arrays;
import java.util.List;

public class Reactions {
    /**
     * List of reactions representing classes
     */
    static String[] specs = {
            "Guardian", // 742284992717127722
            "Dragonhunter", // 742284992691961885
            "Firebrand", // 742284992910065694
            "Revenant", // 742284993274839071
            "Herald", // 742284992893419520
            "Renegade", // 742284992880705606
            "Warrior", // 742284993019117580
            "Berserker", // 742284992469794958
            "Spellbreaker", // 742284993065123842
            "Engineer", // 742284992851345435
            "Scrapper", // 742284992977043536
            "Holosmith", // 742284992884768838
            "Ranger", // 742284995317596190
            "Druid", // 742284992637435925
            "Soulbeast", // 742284992943751218
            "Thief", // 742284993023442995
            "Daredevil", // 742284992717127691
            "Deadeye", // 742284992595361793
            "Elementalist", // 742284992406880329
            "Weaver", // 742284992712802396
            "Tempest", // 742284992947683339
            "Mesmer", // 742284993056997376
            "Chronomancer", // 742284992452755528
            "Mirage", // 742284992624722031
            "Necromancer", // 742284993170243594
            "Reaper", // 742284992553680938
            "Scourge" // 742284992931037234
    };
    
    public static String[] coreClasses = {
            "Guardian", // 742284992717127722
            "Revenant", // 742284993274839071
            "Warrior", // 742284993019117580
            "Engineer", // 742284992851345435
            "Ranger", // 742284995317596190
            "Thief", // 742284993023442995
            "Elementalist", // 742284992406880329
            "Mesmer", // 742284993056997376
            "Necromancer" // 742284993170243594
    };

    static Emote[] reactions = {
            getEmoji("742284992717127722"), // Guardian
            getEmoji("742284992691961885"), // Dragonhunter
            getEmoji("742284992910065694"), // Firebrand
            getEmoji("742284993274839071"), // Revenant
            getEmoji("742284992893419520"), // Herald
            getEmoji("742284992880705606"), // Renegade
            getEmoji("742284993019117580"), // Warrior
            getEmoji("742284992469794958"), // Berserker
            getEmoji("742284993065123842"), // Spellbreaker
            getEmoji("742284992851345435"), // Engineer
            getEmoji("742284992977043536"), // Scrapper
            getEmoji("742284992884768838"), // Holosmith
            getEmoji("742284995317596190"), // Ranger
            getEmoji("742284992637435925"), // Druid
            getEmoji("742284992943751218"), // Soulbeast
            getEmoji("742284993023442995"), // Thief
            getEmoji("742284992717127691"), // Daredevil
            getEmoji("742284992595361793"), // Deadeye
            getEmoji("742284992406880329"), // Elementalist
            getEmoji("742284992947683339"), // Tempest
            getEmoji("742284992712802396"), // Weaver
            getEmoji("742284993056997376"), // Mesmer
            getEmoji("742284992452755528"), // Chronomancer
            getEmoji("742284992624722031"), // Mirage
            getEmoji("742284993170243594"), // Necromancer
            getEmoji("742284992553680938"), // Reaper
            getEmoji("742284992931037234"), // Scourge 
            getEmoji("742284992931037294"), // Flex
            getEmoji("742284992830242827"), // Swap
			getEmoji("742284993228701797") // X_
    };

    static Emote[] reactionsCore = {
            getEmoji("742284992717127722"), // Guardian
            getEmoji("742284993274839071"), // Revenant
            getEmoji("742284993019117580"), // Warrior
            getEmoji("742284992851345435"), // Engineer
            getEmoji("742284995317596190"), // Ranger
            getEmoji("742284993023442995"), // Thief
            getEmoji("742284992406880329"), // Elementalist
            getEmoji("742284993056997376"), // Mesmer
            getEmoji("742284993170243594"), // Necromancer
            getEmoji("742284992931037294"), // Flex
            getEmoji("742284992830242827"), // Swap
            getEmoji("742284993228701797") // X_
    };

    static Emote[] reactionsOpenWorld = {
			getEmoji("742284992352223293"), // Check
            getEmoji("742284993228701797") // X_
    };

    /**
     * Get an emoji from it's emote ID via JDA
     *
     * @param id The ID of the emoji
     * @return The emote object representing that emoji
     */
    private static Emote getEmoji(String id) {
        return RaidBot.getInstance().getJda().getEmoteById(id);
    }

    /**
     * Get the list of reaction names as a list
     *
     * @return The list of reactions as a list
     */
    public static List<String> getSpecs() {
        return new ArrayList<>(Arrays.asList(specs));
    }

    /**
     * Get the list of emote objects
     *
     * @return The emotes
     */
    public static List<Emote> getEmotes() {
        return new ArrayList<>(Arrays.asList(reactions));
    }

    /**
     * Get the list of core class emote objects
     *
     * @return The emotes
     */
    public static List<Emote> getCoreClassEmotes() {
        return new ArrayList<>(Arrays.asList(reactionsCore));
    }
    
    /**
     * Get the list of open world emote objects
     *
     * @return The emotes
     */
    public static List<Emote> getOpenWorldEmotes() {
        return new ArrayList<>(Arrays.asList(reactionsOpenWorld));
    }

    public static Emote getEmoteByName(String name) {
        for (Emote emote : reactions) {
            if (emote != null && emote.getName().equalsIgnoreCase(name)) {
                return emote;
            }
        }
        return null;
    }
}
