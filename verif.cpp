#include <iostream>
#include <fstream>
#include <string>
#include <functional>
#include <cstdio>
#include <unistd.h>

#include "solution.hpp"

#include "CLI11.hpp"


void monMain(std::filesystem::path carte) {
    Environement env(carte);
    char action;
    while(std::cin >> action) {
        if(env.actionner(action) == false) {
            std::cerr << "Vérificateur: Action invalide reçue de l'agent: " << action << std::endl;
            exit(-1);
        }
        if(action == 'q') {
            break;
        }
    }
    //env.afficher_stats("Vérificateur: ");
    auto stats_tool = env.get_stats();

    {
        Environement env2(carte);

        Etat depart = env2.get_etat_courant();
        auto [pos, actions] = env2.dijkstra([&](const Etat & etat) {
            return env2.has_gold_at(etat);
        });

        for(const auto & a : actions) {
            env2.actionner(a);
        }

        env2.actionner('s');
        // Trouver la meilleur suite d'action pour revenir au point de départ
        auto [pos_retour, actions_retour] = env2.dijkstra([&](const Etat & etat) {
            return etat.position_agent == depart.position_agent;
        });
        for(const auto & a : actions_retour) {
            env2.actionner(a);
        }
        env2.actionner('q');

        auto stats_ideal = env2.get_stats();

        if(stats_ideal < stats_tool) {
            std::cerr << "Vérificateur: L'agent n'a pas trouvé la solution optimale." << std::endl;
            std::cerr << "Vérificateur: Statistiques de l'agent:" << std::endl;
            env.afficher_stats("Vérificateur: ");
            std::cerr << "Vérificateur: Statistiques de la solution idéale:" << std::endl;
            env2.afficher_stats("Vérificateur: ");
        } else if(stats_ideal == stats_tool) {
            std::cerr << "Vérificateur: L'agent a trouvé une solution optimale." << std::endl;
        } else {
            std::cerr << "Vérificateur: Il semble y avoir une erreur dans mon vérificateur. Merci de me prévenir par courriel en joignant le fichier de carte utilisé et la solution retourné par votre outil." << std::endl;
        }
    }
}


int main(int argc, char *argv[])
{
    CLI::App app("Verificateur pour le jeu du Wumpus");

    std::filesystem::path votre_programme;
    app.add_option("VotreProgramme", votre_programme, "Executable de votre agent")->check(CLI::ExistingFile)->required();

    std::filesystem::path carte;
    app.add_option("Carte", carte, "Executable de votre agent")->check(CLI::ExistingFile)->required();
    
    CLI11_PARSE(app, argc, argv);

    votre_programme = std::filesystem::absolute(votre_programme);
    carte = std::filesystem::absolute(carte);
    
    // Create a pipe
    int pipefd_child2parent[2];
    pipe(pipefd_child2parent);

    // Create a pipe
    int pipefd_parent2child[2];
    pipe(pipefd_parent2child);

    // Fork the process
    pid_t pid = fork();

    if (pid == 0)
    {
        // Child process
        close(pipefd_child2parent[1]);
        close(pipefd_parent2child[0]);

        // Redirect cout to the write end of the pipe
        dup2(pipefd_parent2child[1], STDOUT_FILENO);
        dup2(pipefd_child2parent[0], STDIN_FILENO);

        std::string s = "\"" + votre_programme.string() + "\" " + "\"" + carte.string() + "\"";
        system(s.c_str());

        // Close the pipes
        close(pipefd_child2parent[0]);
        close(pipefd_parent2child[1]);
    } else {
        close(pipefd_child2parent[0]);
        close(pipefd_parent2child[1]);

        // Redirect cout to the write end of the pipe
        dup2(pipefd_child2parent[1], STDOUT_FILENO);
        dup2(pipefd_parent2child[0], STDIN_FILENO);

        monMain(carte);

        // Close the pipes
        close(pipefd_child2parent[1]);
        close(pipefd_parent2child[0]);
    }
}